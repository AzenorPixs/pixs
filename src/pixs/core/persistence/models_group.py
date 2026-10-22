"""Groupes Core : périmètre stocké avec scope optionnel, relations par PK technique + UNIQUE."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.persistence.base import UUID7_RE, CoreBase
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7

FIXED_MESSAGE = "Groupe Core invalide."


class CoreGroup(CoreBase):
    group_id = models.UUIDField(primary_key=True, editable=False)
    scope_type = models.TextField()
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name="+",
        db_column="tenant_id",
    )
    scope = models.ForeignKey(
        "pixs_core.CoreScope",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name="+",
        db_column="scope_id",
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_group"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=models.Q(group_id__regex=UUID7_RE), name="grp_uuid7_rgx"),
            models.CheckConstraint(
                condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="grp_scope_vocab"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(scope_type="TENANT", tenant__isnull=False)
                    | models.Q(scope_type="PLATFORM", tenant__isnull=True, scope__isnull=True)
                ),
                name="grp_tenant_coherence",
            ),
        ]
        indexes = [models.Index(fields=["tenant"], name="grp_tenant_ix")]

    def clean(self) -> None:
        # Même tenant groupe/scope : validation privée + garde service sous verrou,
        # pas de CHECK inter-table. PLATFORM : tenant et scope absents.
        try:
            check_uuid7(self.group_id)
        except Uuid7Error as error:
            raise ValidationError(FIXED_MESSAGE) from error
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            raise ValidationError(FIXED_MESSAGE)
        if self.scope_type == "PLATFORM":
            if self.tenant_id is not None or self.scope_id is not None:
                raise ValidationError(FIXED_MESSAGE)
        elif type(self.tenant_id) is not str or self.tenant_id == "":
            raise ValidationError(FIXED_MESSAGE)
        if self.scope_id is not None and (type(self.scope_id) is not str or self.scope_id == ""):
            raise ValidationError(FIXED_MESSAGE)


class CoreUserGroupMembership(CoreBase):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("pixs_core.CoreUser", on_delete=models.PROTECT, related_name="+")
    group = models.ForeignKey(CoreGroup, on_delete=models.PROTECT, related_name="+")


    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_ugroup"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["user", "group"], name="ugroup_user_grp_uq", condition=models.Q(persistence_state="ACTIVE")),
        ]


class CoreIdentityTenantMembership(CoreBase):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(
        "pixs_core.CoreIdentity", on_delete=models.PROTECT, related_name="+"
    )
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant", on_delete=models.PROTECT, related_name="+", db_column="tenant_id"
    )
    # Sans défaut implicite : la mutation fournit explicitement ACTIVE ou REVOKED.
    activation = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_idtenant"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["identity", "tenant"], name="idtenant_idt_ten_uq"),
            models.CheckConstraint(
                condition=models.Q(activation__in=["ACTIVE", "REVOKED"]), name="idtenant_act_vocab"
            ),
        ]
