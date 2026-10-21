"""Identités Core : UUIDv7 exacts, R01 unique, sans credential/hash."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.identity.models import DigitalIdentity, IdentityError, IdentityState, IdentityType
from pixs.core.persistence.base import UUID7_RE, CoreBase
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7

FIXED_MESSAGE = "Identité Core invalide."


class CoreUser(CoreBase):
    user_id = models.UUIDField(primary_key=True, editable=False)

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_user"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=models.Q(user_id__regex=UUID7_RE), name="user_uuid7_rgx"),
        ]

    def clean(self) -> None:
        try:
            check_uuid7(self.user_id)
        except Uuid7Error:
            raise ValidationError(FIXED_MESSAGE) from None


class CoreIdentity(CoreBase):
    identity_id = models.UUIDField(primary_key=True, editable=False)
    identity_type = models.TextField()
    state = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_identity"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=models.Q(identity_id__regex=UUID7_RE), name="idt_uuid7_rgx"),
            models.CheckConstraint(
                condition=models.Q(identity_type__in=[t.value for t in IdentityType]),
                name="idt_type_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(state__in=[s.value for s in IdentityState]), name="idt_state_vocab"
            ),
        ]

    def clean(self) -> None:
        raw_type = self.identity_type
        raw_state = self.state
        if type(raw_type) is not str or type(raw_state) is not str:
            raise ValidationError(FIXED_MESSAGE)
        try:
            member_type = IdentityType(raw_type)
        except ValueError:
            raise ValidationError(FIXED_MESSAGE) from None
        try:
            member_state = IdentityState(raw_state)
        except ValueError:
            raise ValidationError(FIXED_MESSAGE) from None
        try:
            check_uuid7(self.identity_id)
        except Uuid7Error:
            raise ValidationError(FIXED_MESSAGE) from None
        try:
            from pixs.core.identity.models import validate_identity

            validate_identity(
                DigitalIdentity(
                    identity_id=self.identity_id, identity_type=member_type, state=member_state
                )
            )
        except IdentityError:
            raise ValidationError(FIXED_MESSAGE) from None


class CoreIdentityLink(CoreBase):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("pixs_core.CoreUser", on_delete=models.PROTECT, related_name="+")
    identity = models.ForeignKey(
        "pixs_core.CoreIdentity", on_delete=models.PROTECT, related_name="+"
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_idlink"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["user"], name="idlink_user_uq", condition=models.Q(persistence_state="ACTIVE")),
            models.UniqueConstraint(fields=["identity"], name="idlink_idt_uq", condition=models.Q(persistence_state="ACTIVE")),
        ]


class CoreSuperAdminBinding(CoreBase):
    installation_ref = models.TextField(primary_key=True)
    identity = models.ForeignKey(
        "pixs_core.CoreIdentity", on_delete=models.PROTECT, related_name="+"
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_su_binding"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(installation_ref=""), name="subind_nonempty"),
        ]

    def clean(self) -> None:
        if type(self.installation_ref) is not str or self.installation_ref == "":
            raise ValidationError(FIXED_MESSAGE)
        # Refus SERVICE/délégation : garde propriétaire sous verrou (service),
        # sans HUMAN imposé et sans CHECK avec jointure (impossible en CHECK).


class CoreSuperAdminTenantGrant(CoreBase):
    id = models.BigAutoField(primary_key=True)
    binding = models.ForeignKey(
        "pixs_core.CoreSuperAdminBinding",
        on_delete=models.PROTECT,
        related_name="+",
        db_column="installation_ref",
    )
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant", on_delete=models.PROTECT, related_name="+", db_column="tenant_id"
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_su_grant"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["binding", "tenant"], name="sugrant_bind_tenant_uq", condition=models.Q(persistence_state="ACTIVE")),
        ]
