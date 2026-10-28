'''Comparaison pure des liaisons de provisionnement.

Verifie une concordance structurelle avec une cible explicite.
Origine autorisation fraicheur et anti-rejeu ne sont pas prouves.
Aucune confiance ni persistance ni horloge ni effet.
Succes rend None, la sortie n est pas une preuve d autorisation.
'''
from pixs.pa_native.provisioning_contracts import ProvisioningDocument
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
from pixs.pa_native.provisioning_contracts import ProvisioningContractError
from pixs.pa_native.provisioning_contracts import decode_provisioning_document
from pixs.pa_native.provisioning_contracts import encode_provisioning_document
__all__ = ['ProvisioningBindingsError', 'assert_provisioning_bindings', 'decode_and_check_bindings']
class ProvisioningBindingsError(ValueError):
    '''Diagnostic fixe sans donnee ni reference.'''
    def __init__(self):
        self.code = 'BINDINGS_MISMATCH'
        self.element = 'provisioning_bindings'
        self.step = 'check_provisioning_bindings'
        self.message = 'Liaisons non concordantes.'
        super().__init__('Liaisons non concordantes.')
    def __str__(self):
        return 'Liaisons non concordantes.'
    def __repr__(self):
        return 'ProvisioningBindingsError(BINDINGS_MISMATCH)'
def assert_provisioning_bindings(actual: ProvisioningDocument, expected: ProvisioningDocument, limits: ProvisioningLimits) -> None:
    '''Concordance exclusive des octets canoniques, None en succes.'''
    try:
        actual_bytes = encode_provisioning_document(actual, limits)
    except ProvisioningContractError:
        raise ProvisioningBindingsError() from None
    try:
        expected_bytes = encode_provisioning_document(expected, limits)
    except ProvisioningContractError:
        raise ProvisioningBindingsError() from None
    if actual_bytes != expected_bytes:
        raise ProvisioningBindingsError()
    return None
def decode_and_check_bindings(data: bytes, expected: ProvisioningDocument, limits: ProvisioningLimits) -> ProvisioningDocument:
    '''Decode puis controle, profil valide avant analyse.'''
    try:
        document = decode_provisioning_document(data, limits)
    except ProvisioningContractError:
        raise ProvisioningBindingsError() from None
    assert_provisioning_bindings(document, expected, limits)
    return document
