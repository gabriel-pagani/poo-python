CREATE PROCEDURE CRIPTOGRAFIA
    @ID INT,
    @NUMERO_CARTAO CHAR(16),
    @NOME_CARTAO VARCHAR(100),
    @VENCIMENTO_CARTAO CHAR(5),
    @CODIGO_CARTAO CHAR(3)
AS BEGIN
    OPEN SYMMETRIC KEY CHAVE DECRYPTION BY CERTIFICATE CERTIFICADO;
    
    DECLARE @ULTIMOS_DIGITOS CHAR(4) = RIGHT(@NUMERO_CARTAO, 4);
    
    UPDATE USUARIOS
    SET 
        NUMERO_CARTAO = ENCRYPTBYKEY(KEY_GUID('CHAVE'), @NUMERO_CARTAO),
        NOME_CARTAO = ENCRYPTBYKEY(KEY_GUID('CHAVE'), @NOME_CARTAO),
        VENCIMENTO_CARTAO = ENCRYPTBYKEY(KEY_GUID('CHAVE'), @VENCIMENTO_CARTAO),
        CODIGO_CARTAO = ENCRYPTBYKEY(KEY_GUID('CHAVE'), @CODIGO_CARTAO),
        ULTIMOS_DIGITOS_CARTAO = @ULTIMOS_DIGITOS
    WHERE ID = @ID;
    
    CLOSE SYMMETRIC KEY CHAVE;
END;

/*
Exemplo de uso do procedimento

EXEC CRIPTOGRAFIA
    @ID = 1
    @NUMERO_CARTAO = '1234567890123456',
    @NOME_CARTAO = 'NOME DO TITULAR',
    @VENCIMENTO_CARTAO = '12/25',
    @CODIGO_CARTAO = '123';
*/