"""PZT CA 0002 garanties registre, PostgreSQL seulement, DDL seule."""
from django.db import migrations


def check_postgresql(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        raise RuntimeError("PZT_CA_POSTGRESQL_REQUIS")


FORWARD = """
CREATE OR REPLACE FUNCTION pzt_ca_forbid_delete()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'PZT_CA_DELETE_FORBIDDEN' USING ERRCODE='23514';
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_key_material()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.key_ref,OLD.key_material_ref,OLD.spki_sha256,OLD.spki_der,OLD.key_created_at,OLD.ca_kind,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.key_ref,NEW.key_material_ref,NEW.spki_sha256,NEW.spki_der,NEW.key_created_at,NEW.ca_kind,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_root()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.domain,OLD.root_ref,OLD.root_generation_id,OLD.root_cert_ref,OLD.key_material_id,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.domain,NEW.root_ref,NEW.root_generation_id,NEW.root_cert_ref,NEW.key_material_id,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  IF OLD.status IS DISTINCT FROM NEW.status THEN
    IF OLD.status='retired' THEN RAISE EXCEPTION 'PZT_CA_RETIRED_TERMINAL' USING ERRCODE='23514'; END IF;
  END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_issuer()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.domain,OLD.logical_authority,OLD.emission_scope,OLD.issuer_id,OLD.issuer_role,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.domain,NEW.logical_authority,NEW.emission_scope,NEW.issuer_id,NEW.issuer_role,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_generation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.issuer_id,OLD.root_id,OLD.key_material_id,OLD.generation_id,OLD.created_epoch,OLD.predecessor_id,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.issuer_id,NEW.root_id,NEW.key_material_id,NEW.generation_id,NEW.created_epoch,NEW.predecessor_id,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  IF OLD.status IS DISTINCT FROM NEW.status THEN
    IF OLD.status='retired' THEN RAISE EXCEPTION 'PZT_CA_RETIRED_TERMINAL' USING ERRCODE='23514'; END IF;
  END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_certificate()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.cert_ref,OLD.cert_bytes_ref,OLD.ca_kind,OLD.root_id,OLD.intermediate_generation_id,OLD.serial_number,OLD.serial_public,OLD.not_before_utc,OLD.not_after_utc,OLD.fingerprint_public,OLD.fingerprint_sha256,OLD.subject_key_id,OLD.ski,OLD.authority_key_id,OLD.aki,OLD.certificate_der,OLD.root_der,OLD.subject_spki_der,OLD.root_spki_der,OLD.anchor_ref,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.cert_ref,NEW.cert_bytes_ref,NEW.ca_kind,NEW.root_id,NEW.intermediate_generation_id,NEW.serial_number,NEW.serial_public,NEW.not_before_utc,NEW.not_after_utc,NEW.fingerprint_public,NEW.fingerprint_sha256,NEW.subject_key_id,NEW.ski,NEW.authority_key_id,NEW.aki,NEW.certificate_der,NEW.root_der,NEW.subject_spki_der,NEW.root_spki_der,NEW.anchor_ref,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_oplink()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.domain,OLD.logical_authority,OLD.emission_scope,OLD.operation_id,OLD.operation_version,OLD.request_id,OLD.context_ref,OLD.input_fingerprint,OLD.epoch,OLD.policy_ref,OLD.content_sha256,OLD.serializer_version,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.domain,NEW.logical_authority,NEW.emission_scope,NEW.operation_id,NEW.operation_version,NEW.request_id,NEW.context_ref,NEW.input_fingerprint,NEW.epoch,NEW.policy_ref,NEW.content_sha256,NEW.serializer_version,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_result()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.result_id,OLD.operation_link_id,OLD.recorded_at,OLD.result_kind,OLD.validation,OLD.engagement,OLD.effect,OLD.error_code,OLD.engagement_ref,OLD.effect_evidence_ref,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.result_id,NEW.operation_link_id,NEW.recorded_at,NEW.result_kind,NEW.validation,NEW.engagement,NEW.effect,NEW.error_code,NEW.engagement_ref,NEW.effect_evidence_ref,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION pzt_ca_guard_retirement()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF ROW(OLD.retirement_ref,OLD.target_root_id,OLD.target_generation_id,OLD.operation_link_id,OLD.retired_at,OLD.epoch,OLD.retirement_evidence_ref,OLD.id,OLD.created_at)
  IS DISTINCT FROM ROW(NEW.retirement_ref,NEW.target_root_id,NEW.target_generation_id,NEW.operation_link_id,NEW.retired_at,NEW.epoch,NEW.retirement_evidence_ref,NEW.id,NEW.created_at)
  THEN RAISE EXCEPTION 'PZT_CA_IMMUTABLE' USING ERRCODE='23514'; END IF;
  RETURN NEW;
END $$;

CREATE TRIGGER pzt_ca_key_material_no_del BEFORE DELETE ON pixs_pzt_ca_key_material FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_key_material_no_upd BEFORE UPDATE ON pixs_pzt_ca_key_material FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_key_material();
CREATE TRIGGER pzt_ca_root_no_del BEFORE DELETE ON pixs_pzt_ca_root FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_root_guard BEFORE UPDATE ON pixs_pzt_ca_root FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_root();
CREATE TRIGGER pzt_ca_issuer_no_del BEFORE DELETE ON pixs_pzt_ca_issuer FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_issuer_no_upd BEFORE UPDATE ON pixs_pzt_ca_issuer FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_issuer();
CREATE TRIGGER pzt_ca_generation_no_del BEFORE DELETE ON pixs_pzt_ca_generation FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_generation_guard BEFORE UPDATE ON pixs_pzt_ca_generation FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_generation();
CREATE TRIGGER pzt_ca_certificate_no_del BEFORE DELETE ON pixs_pzt_ca_certificate FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_certificate_no_upd BEFORE UPDATE ON pixs_pzt_ca_certificate FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_certificate();
CREATE TRIGGER pzt_ca_oplink_no_del BEFORE DELETE ON pixs_pzt_ca_operation_link FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_oplink_no_upd BEFORE UPDATE ON pixs_pzt_ca_operation_link FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_oplink();
CREATE TRIGGER pzt_ca_result_no_del BEFORE DELETE ON pixs_pzt_ca_result_record FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_result_no_upd BEFORE UPDATE ON pixs_pzt_ca_result_record FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_result();
CREATE TRIGGER pzt_ca_retire_no_del BEFORE DELETE ON pixs_pzt_ca_retirement_record FOR EACH ROW EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_retire_no_upd BEFORE UPDATE ON pixs_pzt_ca_retirement_record FOR EACH ROW EXECUTE FUNCTION pzt_ca_guard_retirement();
CREATE TRIGGER pzt_ca_key_material_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_key_material FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_root_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_root FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_issuer_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_issuer FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_generation_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_generation FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_certificate_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_certificate FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_oplink_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_operation_link FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_result_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_result_record FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
CREATE TRIGGER pzt_ca_retire_no_trunc BEFORE TRUNCATE ON pixs_pzt_ca_retirement_record FOR EACH STATEMENT EXECUTE FUNCTION pzt_ca_forbid_delete();
"""

REVERSE = """
DROP TRIGGER IF EXISTS pzt_ca_key_material_no_trunc ON pixs_pzt_ca_key_material;
DROP TRIGGER IF EXISTS pzt_ca_root_no_trunc ON pixs_pzt_ca_root;
DROP TRIGGER IF EXISTS pzt_ca_issuer_no_trunc ON pixs_pzt_ca_issuer;
DROP TRIGGER IF EXISTS pzt_ca_generation_no_trunc ON pixs_pzt_ca_generation;
DROP TRIGGER IF EXISTS pzt_ca_certificate_no_trunc ON pixs_pzt_ca_certificate;
DROP TRIGGER IF EXISTS pzt_ca_oplink_no_trunc ON pixs_pzt_ca_operation_link;
DROP TRIGGER IF EXISTS pzt_ca_result_no_trunc ON pixs_pzt_ca_result_record;
DROP TRIGGER IF EXISTS pzt_ca_retire_no_trunc ON pixs_pzt_ca_retirement_record;
DROP TRIGGER IF EXISTS pzt_ca_retire_no_upd ON pixs_pzt_ca_retirement_record;
DROP TRIGGER IF EXISTS pzt_ca_retire_no_del ON pixs_pzt_ca_retirement_record;
DROP TRIGGER IF EXISTS pzt_ca_result_no_upd ON pixs_pzt_ca_result_record;
DROP TRIGGER IF EXISTS pzt_ca_result_no_del ON pixs_pzt_ca_result_record;
DROP TRIGGER IF EXISTS pzt_ca_oplink_no_upd ON pixs_pzt_ca_operation_link;
DROP TRIGGER IF EXISTS pzt_ca_oplink_no_del ON pixs_pzt_ca_operation_link;
DROP TRIGGER IF EXISTS pzt_ca_certificate_no_upd ON pixs_pzt_ca_certificate;
DROP TRIGGER IF EXISTS pzt_ca_certificate_no_del ON pixs_pzt_ca_certificate;
DROP TRIGGER IF EXISTS pzt_ca_generation_guard ON pixs_pzt_ca_generation;
DROP TRIGGER IF EXISTS pzt_ca_generation_no_del ON pixs_pzt_ca_generation;
DROP TRIGGER IF EXISTS pzt_ca_issuer_no_upd ON pixs_pzt_ca_issuer;
DROP TRIGGER IF EXISTS pzt_ca_issuer_no_del ON pixs_pzt_ca_issuer;
DROP TRIGGER IF EXISTS pzt_ca_root_guard ON pixs_pzt_ca_root;
DROP TRIGGER IF EXISTS pzt_ca_root_no_del ON pixs_pzt_ca_root;
DROP TRIGGER IF EXISTS pzt_ca_key_material_no_upd ON pixs_pzt_ca_key_material;
DROP TRIGGER IF EXISTS pzt_ca_key_material_no_del ON pixs_pzt_ca_key_material;
DROP FUNCTION IF EXISTS pzt_ca_guard_retirement();
DROP FUNCTION IF EXISTS pzt_ca_guard_result();
DROP FUNCTION IF EXISTS pzt_ca_guard_oplink();
DROP FUNCTION IF EXISTS pzt_ca_guard_certificate();
DROP FUNCTION IF EXISTS pzt_ca_guard_generation();
DROP FUNCTION IF EXISTS pzt_ca_guard_issuer();
DROP FUNCTION IF EXISTS pzt_ca_guard_root();
DROP FUNCTION IF EXISTS pzt_ca_guard_key_material();
DROP FUNCTION IF EXISTS pzt_ca_forbid_delete();
"""

class Migration(migrations.Migration):
    dependencies = [("pixs_pzt_ca", "0001_initial")]
    operations = [
        migrations.RunPython(check_postgresql, migrations.RunPython.noop),
        migrations.RunSQL(sql=FORWARD, reverse_sql=REVERSE),
    ]
