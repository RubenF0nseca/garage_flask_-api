-- Tabela de clientes
CREATE TABLE client (
    client_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

-- Tabela de funcionários
CREATE TABLE employee (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    role TEXT CHECK (role IN ('mechanic', 'manager', 'admin')) DEFAULT 'mechanic',
    hired_date DATE NOT NULL,
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

-- Inserir dados na tabela de clientes
INSERT INTO client (name, email, phone, address) VALUES
('João Silva', 'joao.silva@example.com', '912345678', 'Rua A, 123, Lisboa'),
('Maria Oliveira', 'maria.oliveira@example.com', '913456789', 'Av. B, 456, Porto'),
('Carlos Santos', 'carlos.santos@example.com', '914567890', 'Rua C, 789, Faro'),
('Ana Pereira', 'ana.pereira@example.com', '915678901', 'Rua D, 321, Coimbra'),
('Ricardo Gonçalves', 'ricardo.goncalves@example.com', '916789012', 'Av. E, 654, Braga');


-- Inserir dados na tabela de funcionários
INSERT INTO employee (name, email, phone, role, hired_date) VALUES
('Rui Ferreira', 'rui.ferreira@example.com', '910123456', 'mechanic', '2023-01-15'),
('Ana Costa', 'ana.costa@example.com', '911234567', 'manager', '2022-06-10'),
('Pedro Martins', 'pedro.martins@example.com', '912345678', 'mechanic', '2024-02-20'),
('Tiago Almeida', 'tiago.almeida@example.com', '913456789', 'mechanic', '2024-03-10'),
('Sofia Lopes', 'sofia.lopes@example.com', '914567890', 'admin', '2021-11-01');
