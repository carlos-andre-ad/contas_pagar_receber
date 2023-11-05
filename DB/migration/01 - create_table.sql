
DROP TABLE IF EXISTS public.contas_pagar;
CREATE TABLE public.contas_pagar (
  id serial NOT NULL,
  descricao varchar(100) COLLATE pg_catalog.default NOT NULL,
  observacoes text COLLATE pg_catalog.default,
  data_pagamento date NOT NULL,
  data_vencimento date NOT NULL,
  valor float8 NOT NULL,
  valor_pago float8 NOT NULL,
  id_organizacao int4 NOT NULL);


DROP TABLE IF EXISTS public.contas_receber;
CREATE TABLE public.contas_receber (
  id serial NOT NULL,
  descricao varchar(100) COLLATE pg_catalog.default NOT NULL,
  observacoes text COLLATE pg_catalog.default,
  data_recebimento date NOT NULL,
  valor float8 NOT NULL,
  id_organizacao int4 NOT NULL);



DROP TABLE IF EXISTS public.pessoa;
CREATE TABLE public.pessoa (
  id serial NOT NULL,
  nome varchar(100) COLLATE pg_catalog.default NOT NULL,
  id_organizacao int4,
  tipo_fornecedor bool DEFAULT false,
  tipo_prestador bool DEFAULT false,
  tipo_cliente bool DEFAULT false,
  tipo_instit_financ bool DEFAULT false);
  
  
DROP TABLE IF EXISTS public.usuario;
CREATE TABLE public.usuario (
  id serial NOT NULL,
  email varchar(255) COLLATE pg_catalog.default NOT NULL,
  senha varchar(255) COLLATE pg_catalog.default NOT NULL);



-- ----------------------------
-- Primary Key structure for table contas_pagar
-- ----------------------------
ALTER TABLE public.contas_pagar ADD CONSTRAINT contas_pagar_id_pk PRIMARY KEY (id);

-- ----------------------------
-- Primary Key structure for table contas_receber
-- ----------------------------
ALTER TABLE public.contas_receber ADD CONSTRAINT contas_preceber_id_pk PRIMARY KEY (id);

-- ----------------------------
-- Uniques structure for table pessoa
-- ----------------------------
ALTER TABLE public.pessoa ADD CONSTRAINT nome_organizacao_uniq UNIQUE (nome);

-- ----------------------------
-- Primary Key structure for table pessoa
-- ----------------------------
ALTER TABLE public.pessoa ADD CONSTRAINT pessoa_id_pk PRIMARY KEY (id);

-- ----------------------------
-- Primary Key structure for table usuario
-- ----------------------------
ALTER TABLE public.usuario ADD CONSTRAINT usuario_id_pk PRIMARY KEY (id);

-- ----------------------------
-- Foreign Keys structure for table contas_pagar
-- ----------------------------
ALTER TABLE public.contas_pagar ADD CONSTRAINT fk_id_organizacao FOREIGN KEY (id_organizacao) REFERENCES public.pessoa (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table contas_receber
-- ----------------------------
ALTER TABLE public.contas_receber ADD CONSTRAINT fk_id_organizacao_rec FOREIGN KEY (id_organizacao) REFERENCES public.pessoa (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

