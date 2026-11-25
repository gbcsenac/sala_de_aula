-- dados_de_exemplo.sql — jogos, clientes e aluguéis para a janela ter o que
-- mostrar. Só no banco "locadora", nunca no "locadora_teste": o teste apaga
-- tudo antes de rodar.
--
-- No pgAdmin: clique com o botão direito no banco "locadora" → Query Tool →
-- abra este arquivo (ícone da pasta) → ▶. Rode o criar_tabelas.sql antes.
--
-- Pode rodar de novo sem estragar nada: o ON CONFLICT DO NOTHING pula o que já
-- existe, apoiado nas UNIQUE de cada tabela. As datas são fixas de propósito:
-- com CURRENT_DATE, rodar amanhã criaria aluguéis novos, porque a data de
-- retirada faz parte da chave natural do empréstimo.

INSERT INTO jogo (titulo, genero, ano_lancamento, preco_diaria) VALUES
    ('The Legend of Zelda', 'Aventura', 2017, 8.50),
    ('FIFA 25', 'Esporte', 2024, 9.00),
    ('Mario Kart 8', 'Corrida', 2017, 7.00),
    ('God of War Ragnarök', 'Ação', 2022, 10.00),
    ('Stardew Valley', 'Simulação', 2016, 5.00),
    ('Minecraft', 'Aventura', 2011, 6.00)
ON CONFLICT DO NOTHING;

INSERT INTO cliente (nome, telefone, email) VALUES
    ('Marcos Pereira', '(51) 99812-3344', 'marcos@exemplo.com'),
    ('Júlia Ramos', '(51) 98455-1020', 'julia@exemplo.com'),
    ('Rafael Costa', '(51) 99107-8866', 'rafael@exemplo.com'),
    ('Beatriz Nunes', '(51) 98230-4511', 'beatriz@exemplo.com')
ON CONFLICT DO NOTHING;

-- O id do cliente é procurado pelo nome, e não escrito como 1, 2, 3: o id é do
-- banco, e muda se alguém cadastrou outro cliente antes.
INSERT INTO emprestimo (id_cliente, data_retirada, data_prevista, data_entregue, multa)
SELECT c.id_cliente, e.retirada, e.prevista, e.entregue, e.multa
FROM (VALUES
    -- o histórico de outubro, já devolvido: é o que dá número ao Resumo
    ('Marcos Pereira', DATE '2026-10-02', DATE '2026-10-05', DATE '2026-10-05', 0.00),
    ('Júlia Ramos',    DATE '2026-10-04', DATE '2026-10-06', DATE '2026-10-06', 0.00),
    ('Rafael Costa',   DATE '2026-10-09', DATE '2026-10-12', DATE '2026-10-16', 20.00),
    ('Beatriz Nunes',  DATE '2026-10-16', DATE '2026-10-19', DATE '2026-10-19', 0.00),
    ('Marcos Pereira', DATE '2026-10-23', DATE '2026-10-26', DATE '2026-10-26', 0.00),
    ('Júlia Ramos',    DATE '2026-10-30', DATE '2026-11-02', DATE '2026-11-02', 0.00),
    -- devolvido em dia: não aparece nos atrasados
    ('Marcos Pereira', DATE '2026-11-03', DATE '2026-11-06', DATE '2026-11-06', 0.00),
    -- atrasados, ainda com o jogo em casa
    ('Júlia Ramos',    DATE '2026-11-10', DATE '2026-11-13', NULL, 0.00),
    ('Rafael Costa',   DATE '2026-11-14', DATE '2026-11-17', NULL, 0.00),
    -- no prazo
    ('Beatriz Nunes',  DATE '2026-11-18', DATE '2026-12-01', NULL, 0.00)
) AS e (nome, retirada, prevista, entregue, multa)
JOIN cliente c ON c.nome = e.nome
ON CONFLICT DO NOTHING;

INSERT INTO item_emprestimo (id_emprestimo, id_jogo, preco_pago)
SELECT em.id_emprestimo, j.id_jogo, i.preco_pago
FROM (VALUES
    ('Marcos Pereira', DATE '2026-10-02', 'FIFA 25', 27.00),
    ('Marcos Pereira', DATE '2026-10-02', 'Mario Kart 8', 21.00),
    ('Júlia Ramos',    DATE '2026-10-04', 'The Legend of Zelda', 17.00),
    ('Rafael Costa',   DATE '2026-10-09', 'FIFA 25', 27.00),
    ('Rafael Costa',   DATE '2026-10-09', 'God of War Ragnarök', 30.00),
    ('Beatriz Nunes',  DATE '2026-10-16', 'Minecraft', 18.00),
    ('Marcos Pereira', DATE '2026-10-23', 'FIFA 25', 27.00),
    ('Júlia Ramos',    DATE '2026-10-30', 'Mario Kart 8', 21.00),
    ('Marcos Pereira', DATE '2026-11-03', 'FIFA 25', 27.00),
    ('Júlia Ramos',    DATE '2026-11-10', 'The Legend of Zelda', 25.50),
    ('Júlia Ramos',    DATE '2026-11-10', 'Mario Kart 8', 21.00),
    ('Rafael Costa',   DATE '2026-11-14', 'God of War Ragnarök', 30.00),
    ('Beatriz Nunes',  DATE '2026-11-18', 'Stardew Valley', 65.00)
) AS i (nome, retirada, titulo, preco_pago)
JOIN cliente c     ON c.nome = i.nome
JOIN emprestimo em ON em.id_cliente = c.id_cliente AND em.data_retirada = i.retirada
JOIN jogo j        ON j.titulo = i.titulo
ON CONFLICT DO NOTHING;

-- Conferência: 6 jogos, 4 clientes, 10 empréstimos, 13 itens. Se dobrarem ao
-- rodar de novo, alguma UNIQUE do criar_tabelas.sql não foi criada.
SELECT
    (SELECT COUNT(*) FROM jogo)            AS jogos,
    (SELECT COUNT(*) FROM cliente)         AS clientes,
    (SELECT COUNT(*) FROM emprestimo)      AS emprestimos,
    (SELECT COUNT(*) FROM item_emprestimo) AS itens;
