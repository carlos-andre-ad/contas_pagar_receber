/*
 Navicat Premium Data Transfer

 Source Server         : DESENV
 Source Server Type    : PostgreSQL
 Source Server Version : 130012 (130012)
 Source Host           : localhost:15432
 Source Catalog        : contas
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 130012 (130012)
 File Encoding         : 65001

 Date: 29/10/2023 02:03:31
*/


-- ----------------------------
-- Sequence structure for contas_pagar_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."contas_pagar_id_seq";
CREATE SEQUENCE "public"."contas_pagar_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for contas_pagar_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."contas_pagar_id_seq1";
CREATE SEQUENCE "public"."contas_pagar_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for contas_receber_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."contas_receber_id_seq";
CREATE SEQUENCE "public"."contas_receber_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for contas_receber_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."contas_receber_id_seq1";
CREATE SEQUENCE "public"."contas_receber_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;


-- ----------------------------
-- Sequence structure for pessoa_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pessoa_id_seq";
CREATE SEQUENCE "public"."pessoa_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for pessoa_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pessoa_id_seq1";
CREATE SEQUENCE "public"."pessoa_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for contas_pagar
-- ----------------------------
DROP TABLE IF EXISTS "public"."contas_pagar";
CREATE TABLE "public"."contas_pagar" (
  "id" int4 NOT NULL GENERATED ALWAYS AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "descricao" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "observacoes" text COLLATE "pg_catalog"."default",
  "data_pagamento" date NOT NULL,
  "data_vencimento" date NOT NULL,
  "valor" float8 NOT NULL,
  "valor_pago" float8 NOT NULL,
  "id_organizacao" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for contas_receber
-- ----------------------------
DROP TABLE IF EXISTS "public"."contas_receber";
CREATE TABLE "public"."contas_receber" (
  "id" int4 NOT NULL GENERATED ALWAYS AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "descricao" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "observacoes" text COLLATE "pg_catalog"."default",
  "data_recebimento" date NOT NULL,
  "valor" float8 NOT NULL,
  "id_organizacao" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for pessoa
-- ----------------------------
DROP TABLE IF EXISTS "public"."pessoa";
CREATE TABLE "public"."pessoa" (
  "id" int4 NOT NULL GENERATED ALWAYS AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "nome" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "id_organizacao" int4,
  "tipo_fornecedor" bool,
  "tipo_prestador" bool,
  "tipo_cliente" bool,
  "tipo_instit_financ" bool
)
;

-- ----------------------------
-- Uniques structure for table pessoa
-- ----------------------------
ALTER TABLE "public"."pessoa" ADD CONSTRAINT "nome_organizacao_uniq" UNIQUE ("nome");

-- ----------------------------
-- Primary Key structure for table pessoa
-- ----------------------------
ALTER TABLE "public"."pessoa" ADD CONSTRAINT "pessoa_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table contas_pagar
-- ----------------------------
ALTER TABLE "public"."contas_pagar" ADD CONSTRAINT "fk_id_organizacao" FOREIGN KEY ("id_organizacao") REFERENCES "public"."pessoa" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table contas_receber
-- ----------------------------
ALTER TABLE "public"."contas_receber" ADD CONSTRAINT "fk_id_organizacao_rec" FOREIGN KEY ("id_organizacao") REFERENCES "public"."pessoa" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
