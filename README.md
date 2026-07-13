# pontos para a reunião:
## estrutura do Eventos:
-- Script de migração para a tabela Evento
-- Alinhado com o SQLAlchemy 2.0 e Pydantic v2

CREATE TABLE IF NOT EXISTS "Evento" (
    -- 1. Campos de controle gerados automaticamente pelo Banco de Dados
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- 2. Campos Obrigatórios
    titulo TEXT NOT NULL UNIQUE,
    data TIMESTAMP NOT NULL,
    usuario_criador INTEGER NOT NULL,
    tipo_evento INTEGER NOT NULL,
    foto_evento INTEGER NOT NULL,

    -- 3. Campos Opcionais (Aceitam valores Nulos por padrão)
    descricao TEXT DEFAULT NULL,
    capacidade_maxima INTEGER DEFAULT NULL,
    endereco TEXT DEFAULT NULL,
    status TEXT DEFAULT NULL,
    unidade_associated INTEGER DEFAULT NULL,
    data_cancelamento DATE DEFAULT NULL,
    data_ultima_atualizacao DATE DEFAULT NULL,
    link_externo TEXT DEFAULT NULL
);

-- Índices recomendados para otimização de buscas frequentes da API
CREATE INDEX IF NOT EXISTS idx_evento_titulo ON "Evento"(titulo);
CREATE INDEX IF NOT EXISTS idx_evento_usuario_criador ON "Evento"(usuario_criador);