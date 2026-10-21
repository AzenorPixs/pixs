"""Tenants/scopes Core : scope_id PK globalement unique, tenant opaque sans trim."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.persistence.base import CoreBase

FIXED_MESSAGE = "Tenant ou scope Core invalide."


class CoreTenant(CoreBase):
    tenant_id = models.TextField(primary_key=True)

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_tenant"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(tenant_id=""), name="tenant_nonempty"),
        ]

    def clean(self) -> None:
        if type(self.tenant_id) is not str or self.tenant_id == "":
            raise ValidationError(FIXED_MESSAGE)


class CoreScope(CoreBase):
    scope_id = models.TextField(primary_key=True)
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant", on_delete=models.PROTECT, related_name="+", db_column="tenant_id"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name="+",
        db_column="parent_scope_id",
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_scope"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(scope_id=""), name="scope_nonempty"),
            models.UniqueConstraint(fields=["scope_id", "tenant"], name="scope_id_tenant_uq"),
        ]
        indexes = [models.Index(fields=["tenant", "parent"], name="scope_tenant_parent_ix")]

    def clean(self) -> None:
        if type(self.scope_id) is not str or self.scope_id == "":
            raise ValidationError(FIXED_MESSAGE)
