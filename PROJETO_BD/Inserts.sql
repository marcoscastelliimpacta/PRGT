INSERT INTO `tabCargos`(`funcao`)
VALUES ('Pedradeiro'), ('Ajudante'), ('Engenheiro');






INSERT INTO `tabServicos` (`servico`)
VALUES('Alvenaria'),
('Forro de Gesso'),
('Elétrica'),
('Hidráulica'),
('Revestimento'),
('Pintura'),
('Acabamento'),
('ArCondicionado');





INSERT INTO `tabStatus_Projetos` (`status_projeto`)
VALUES('Íniciado'),
('Em progresso'),
('Pausado'),
('Concluido');






INSERT INTO `tabTipo_Usuario` (`tipo_usuario`)
VALUES('dev'),
('admin'),
('cliente'),
('blog'),
('assistente');


INSERT INTO `prgt_db`.`tabUsuarios`
(`usuario`, `senha`, `codigo_tipo_usuario`, `data_hora_post`)
VALUES('admin', md5('admin'), 1, now());


INSERT INTO `tabImagens` (`caminho`, `nome_img`, `setor`, `texto_img`, `link`)
VALUES ('/static/imgs/Admin/',	'Projetos.jpg',	'admin',	'Obras / Projetos',	'Projetos'),
	('/static/imgs/Admin/',	'Blog.jpg',	'admin', 'Blog', 'Blog'),
	('/static/imgs/Admin/',	'home.png',	'admin', 'Home Page',	'Home_Page'),
	('/static/imgs/Admin/',	'Funcionarios.jpg',	'admin',	'Funcionarios',	'Funcionarios'),
	('/static/imgs/Admin/',	'Cliente.jpg',	'admin',	'Clientes',	'Clientes');



INSERT INTO `tabPermissao_Admin` (`codigo_img`, `codigo_usuario`)
VALUES (1,	1), (2, 1), (3, 1), (4, 1), (5, 1);
#Os valores do codigo_img podem mudar, mas apenas na primeira vez que forem inseridos



