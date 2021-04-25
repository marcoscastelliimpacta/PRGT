CREATE TABLE `tabCargos` (
  `codigo_cargos` int(11) NOT NULL AUTO_INCREMENT,
  `funcao` varchar(150),
  PRIMARY KEY (`codigo_cargos`)
) ;



CREATE TABLE `tabClientes` (
  `codigo_cli` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_usuario` int(11),
  `nome_cli` varchar(200),
  `email` varchar(200),
  `telefone` bigint(20),
  PRIMARY KEY (`codigo_cli`),
  KEY `fk_usuario` (`codigo_usuario`),
  CONSTRAINT `fk_usuario` FOREIGN KEY (`codigo_usuario`) REFERENCES `tabUsuarios` (`codigo_usuario`)
) ;




CREATE TABLE `tabFuncionarios` (
  `codigo_func` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_usuario` int(11) DEFAULT NULL,
  `nome` varchar(200)  DEFAULT NULL,
  `cpf` bigint(20) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `codigo_funcao` int(11) DEFAULT NULL,
  `codigo_status` int(11) DEFAULT NULL,
  `codigo_status_alocacao` varchar(50) DEFAULT NULL,
  `data_hora_post` datetime DEFAULT NULL,
  PRIMARY KEY (`codigo_func`),
  UNIQUE KEY `codigo_usuario` (`codigo_usuario`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `email` (`email`(150)),
  KEY `fk_funcoe` (`codigo_funcao`),
  CONSTRAINT `fk_funcoe` FOREIGN KEY (`codigo_funcao`) REFERENCES `tabCargos` (`codigo_cargos`),
  CONSTRAINT `fk_o_usuario` FOREIGN KEY (`codigo_usuario`) REFERENCES `tabUsuarios` (`codigo_usuario`)
) ;






CREATE TABLE `tabImagens` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `caminho` varchar(200) DEFAULT NULL,
  `nome_img` varchar(250) DEFAULT NULL,
  `setor` varchar(200) DEFAULT NULL,
  `texto_img` varchar(5000) DEFAULT NULL,
  `link` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
);







CREATE TABLE `tabImagens_Blog` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `caminho` varchar(200) DEFAULT NULL,
  `nome_img` varchar(250) DEFAULT NULL,
  `setor` varchar(200) DEFAULT NULL,
  `data_img` date DEFAULT NULL,
  `titulo_img` varchar(50) DEFAULT NULL,
  `texto_img` varchar(5000) DEFAULT NULL,
  `link` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
);




CREATE TABLE `tabInfo_txt_Site` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `data` varchar(255) DEFAULT NULL,
  `conteudo` longtext,
  `titulocapa` longtext,
  `titulo` longtext,
  `descricao` longtext,
  PRIMARY KEY (`codigo`)
);




CREATE TABLE `tabPermissao_Admin` (
  `codigo_img` int(11) NOT NULL,
  `codigo_usuario` int(11) NOT NULL,
  KEY `fk_imagem` (`codigo_img`),
  KEY `fk_usuarios` (`codigo_usuario`),
  CONSTRAINT `fk_imagem` FOREIGN KEY (`codigo_img`) REFERENCES `tabImagens` (`codigo`),
  CONSTRAINT `fk_usuarios` FOREIGN KEY (`codigo_usuario`) REFERENCES `tabUsuarios` (`codigo_usuario`)
) ;




CREATE TABLE `tabProjetos` (
  `codigo_projeto` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_status` int(11) DEFAULT NULL,
  `codigo_func_responsavel` int(11) DEFAULT NULL,
  `nome_projeto` varchar(150)  DEFAULT NULL,
  `local_projeto` varchar(500) DEFAULT NULL,
  `orcamento` decimal(13,2) DEFAULT NULL,
  `Observacoes` varchar(10000) DEFAULT NULL,
  `prazo_dias` int(11) DEFAULT NULL,
  `data_inicio` date DEFAULT NULL,
  `data_finalizacao` date DEFAULT NULL,
  `data_hora_post` date DEFAULT NULL,
  PRIMARY KEY (`codigo_projeto`)
) ;



CREATE TABLE `tabRel_Cli_Proj` (
  `codigo_relacao` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_projeto` int(11) DEFAULT NULL,
  `codigo_cliente` int(11) DEFAULT NULL,
  PRIMARY KEY (`codigo_relacao`),
  KEY `fk_codigo_projeto` (`codigo_projeto`),
  KEY `fk_codigo_cliente` (`codigo_cliente`),
  CONSTRAINT `fk_codigo_cliente` FOREIGN KEY (`codigo_cliente`) REFERENCES `tabClientes` (`codigo_cli`),
  CONSTRAINT `fk_codigo_projeto` FOREIGN KEY (`codigo_projeto`) REFERENCES `tabProjetos` (`codigo_projeto`)
) ;





CREATE TABLE `tabRel_Func_Proj` (
  `codigo_relacao` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_projeto` int(11) DEFAULT NULL,
  `codigo_func` int(11) DEFAULT NULL,
  `data_hora_post` date DEFAULT NULL,
  PRIMARY KEY (`codigo_relacao`),
  KEY `fk_codigo_projet` (`codigo_projeto`),
  KEY `fk_codigo_fun` (`codigo_func`),
  CONSTRAINT `fk_codigo_fun` FOREIGN KEY (`codigo_func`) REFERENCES `tabFuncionarios` (`codigo_func`),
  CONSTRAINT `fk_codigo_projet` FOREIGN KEY (`codigo_projeto`) REFERENCES `tabProjetos` (`codigo_projeto`)
) ;






CREATE TABLE `tabRel_Servicos_Projetos` (
  `codigo_projeto` int(11) DEFAULT NULL,
  `codigo_servicos` int(11) DEFAULT NULL,
  `porcentagem` int(11) DEFAULT '0',
  KEY `fk_codigo_Projetos` (`codigo_projeto`),
  KEY `fk_codigo_servico` (`codigo_servicos`),
  CONSTRAINT `fk_codigo_Projetos` FOREIGN KEY (`codigo_projeto`) REFERENCES `tabProjetos` (`codigo_projeto`),
  CONSTRAINT `fk_codigo_servico` FOREIGN KEY (`codigo_servicos`) REFERENCES `tabServicos` (`codigo_servicos`)
) ;






CREATE TABLE `tabServicos` (
  `codigo_servicos` int(11) NOT NULL AUTO_INCREMENT,
  `servico` varchar(200) NOT NULL,
  PRIMARY KEY (`codigo_servicos`)
) ;







CREATE TABLE `tabStatus_Projetos` (
  `codigo_status` int(11) NOT NULL AUTO_INCREMENT,
  `status_projeto` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`codigo_status`)
) ;







CREATE TABLE `tabTipo_Usuario` (
  `codigo_tipo_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_usuario` varchar(50) NOT NULL,
  PRIMARY KEY (`codigo_tipo_usuario`)
) ;





CREATE TABLE `tabUsuarios` (
  `codigo_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(100) DEFAULT NULL,
  `senha` varchar(1000) DEFAULT NULL,
  `codigo_tipo_usuario` int(11) DEFAULT NULL,
  `data_hora_post` datetime DEFAULT NULL,
  PRIMARY KEY (`codigo_usuario`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `fk_tipo_usuario` (`codigo_tipo_usuario`),
  CONSTRAINT `fk_tipo_usuario` FOREIGN KEY (`codigo_tipo_usuario`) REFERENCES `tabTipo_Usuario` (`codigo_tipo_usuario`)
) ;


