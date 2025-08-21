from core.utils.password_utils import encrypt_password, verify_password


def test_encrypt_password_correctly():
    """
    Deve criptografar a senha corretamente e verificar a senha com sucesso
    """
    password = "minha_senha"
    hashed = encrypt_password(password)

    assert hashed != password
    assert len(hashed) > len(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Deve falhar ao verificar uma senha incorreta"""
    password = "minha_senha"
    hashed = encrypt_password(password)

    assert verify_password("senha_incorreta", hashed) is False
