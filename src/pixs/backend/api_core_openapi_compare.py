"""Garde de construction : comparaison structurelle des contrats HTTP publiés."""
from __future__ import annotations

from pixs.backend.api import api_major_prefix, check_api_evolution

__all__ = ["CoreOpenApiEvolutionError", "check_core_openapi_evolution"]


class CoreOpenApiEvolutionError(ValueError):
    def __init__(self):
        super().__init__("Évolution OpenAPI Core refusée.")


def _schema_change(before, after, *, request):
    # Les annotations ne portent pas de garantie de compatibilité de schéma.
    left = {k:v for k,v in before.items() if k not in ("description","title","examples")}
    right = {k:v for k,v in after.items() if k not in ("description","title","examples")}
    if left == right:
        return False
    def categories(schema):
        allowed={"object","array","string","integer","fraction","boolean","null"}
        declared=schema.get("type")
        if declared is None:
            return allowed
        declared=declared if type(declared) is list else [declared]
        result=set(declared)
        if "number" in result:
            result.remove("number");result.update(("integer","fraction"))
        return result
    old_types,new_types=categories(left),categories(right)
    if not (old_types<=new_types if request else new_types<=old_types):
        return True
    for key in ("oneOf","anyOf","allOf","const","format","pattern","additionalProperties"):
        if left.get(key) != right.get(key):
            return True
    old_required,new_required=set(left.get("required",())),set(right.get("required",()))
    if (new_required-old_required if request else old_required-new_required):
        return True
    old_props,new_props=left.get("properties",{}),right.get("properties",{})
    if set(old_props)-set(new_props):
        return True
    if not request and left.get("additionalProperties") is False and set(new_props)-set(old_props):
        return True
    for name in set(old_props)&set(new_props):
        if _schema_change(old_props[name],new_props[name],request=request):
            return True
    if "items" in left and ("items" not in right or _schema_change(left["items"],right["items"],request=request)):
        return True
    old_enum,new_enum=left.get("enum"),right.get("enum")
    if old_enum != new_enum:
        if request:
            if new_enum is not None and (old_enum is None or not set(map(repr,old_enum))<=set(map(repr,new_enum))):
                return True
        elif old_enum is not None and (new_enum is None or not set(map(repr,new_enum))<=set(map(repr,old_enum))):
            return True
    for lower in ("minimum","minLength","minItems"):
        old,new=left.get(lower),right.get(lower)
        if request:
            if new is not None and (old is None or new>old):
                return True
        elif old is not None and (new is None or new<old):
            return True
    for upper in ("maximum","maxLength","maxItems"):
        old,new=left.get(upper),right.get(upper)
        if request:
            if new is not None and (old is None or new<old):
                return True
        elif old is not None and (new is None or new>old):
            return True
    handled={"type","required","properties","items","enum","minimum","maximum",
             "minLength","maxLength","minItems","maxItems","description","title","examples",
             "oneOf","anyOf","allOf","const","format","pattern","additionalProperties"}
    return {k:v for k,v in left.items() if k not in handled}!={k:v for k,v in right.items() if k not in handled}


def _expand(schema, components, depth=0):
    if depth>32 or type(schema) is not dict:
        raise CoreOpenApiEvolutionError()
    if "$ref" in schema:
        ref=schema["$ref"]
        if set(schema)!={"$ref"} or type(ref) is not str or not ref.startswith("#/components/schemas/"):
            raise CoreOpenApiEvolutionError()
        key=ref.removeprefix("#/components/schemas/")
        if key not in components:
            raise CoreOpenApiEvolutionError()
        return _expand(components[key],components,depth+1)
    out={}
    for key,value in schema.items():
        if key=="properties":
            out[key]={name:_expand(item,components,depth+1) for name,item in value.items()}
        elif key=="items":
            out[key]=_expand(value,components,depth+1)
        elif key in ("anyOf","oneOf","allOf"):
            out[key]=[_expand(item,components,depth+1) for item in value]
        else:
            out[key]=value
    return out


def _operations(documents, plan):
    from pixs.backend.api_core_openapi import validate_core_openapi_document
    prefix=api_major_prefix(plan)
    result={}
    if type(documents) is not tuple or not documents:
        raise CoreOpenApiEvolutionError()
    for document in documents:
        root=validate_core_openapi_document(plan,document)
        components=root["components"]["schemas"]
        schemes=root["components"]["securitySchemes"]
        for path,methods in root["paths"].items():
            for method,operation in methods.items():
                key=(path[len(prefix):],method)
                if key in result:
                    raise CoreOpenApiEvolutionError()
                security=operation["security"]
                authentication=[{name:schemes[name] for name in requirement} for requirement in security]
                parameters={(p["in"],p["name"].lower() if p["in"]=="header" else p["name"]):
                    {"required":p["required"],"schema":_expand(p["schema"],components)} for p in operation["parameters"]}
                body=operation.get("requestBody")
                result[key]={"security":authentication,"parameters":parameters,
                    "body":None if body is None else {"required":body["required"],
                        "schema":_expand(body["content"]["application/json"]["schema"],components)},
                    "responses":{code:None if "content" not in r else _expand(r["content"]["application/json"]["schema"],components)
                        for code,r in operation["responses"].items()}}
    return result


def check_core_openapi_evolution(previous_plan, proposed_plan, previous_documents, proposed_documents, *, coexistence_doc=None):
    """Le booléen de rupture est calculé depuis les documents, jamais accepté du client."""
    try:
        previous,current=_operations(previous_documents,previous_plan),_operations(proposed_documents,proposed_plan)
        breaking=False
        for key,old in previous.items():
            new=current.get(key)
            if new is None or old["security"]!=new["security"]:
                breaking=True
                continue
            old_params,new_params=old["parameters"],new["parameters"]
            for name,value in old_params.items():
                if name not in new_params or _schema_change(value["schema"],new_params[name]["schema"],request=True):
                    breaking=True
                elif not value["required"] and new_params[name]["required"]:
                    breaking=True
            if any(value["required"] for name,value in new_params.items() if name not in old_params):
                breaking=True
            old_body,new_body=old["body"],new["body"]
            if old_body is None:
                if new_body is not None and new_body["required"]:
                    breaking=True
            elif new_body is None or (not old_body["required"] and new_body["required"]) or _schema_change(old_body["schema"],new_body["schema"],request=True):
                breaking=True
            for status,schema in old["responses"].items():
                if status not in new["responses"]:
                    breaking=True
                elif schema is None or new["responses"][status] is None:
                    if schema != new["responses"][status]:
                        breaking=True
                elif _schema_change(schema,new["responses"][status],request=False):
                    breaking=True
        check_api_evolution(previous_plan,proposed_plan,breaking=breaking,coexistence_doc=coexistence_doc)
    except CoreOpenApiEvolutionError:
        raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError):
        raise CoreOpenApiEvolutionError() from None
    return "CORE_OPENAPI_EVOLUTION_VALID"
