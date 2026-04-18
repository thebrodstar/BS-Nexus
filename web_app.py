CREATE TABLE IF NOT EXISTS cert_uploads (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid, cert_type text, file_url text, uploaded_at timestamptz DEFAULT now(), approved boolean DEFAULT false, approved_by uuid, approved_at timestamptz);

CREATE TABLE IF NOT EXISTS cert_approvals (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid, manager_id uuid, cert_type text, expiry_date text, status text DEFAULT 'Pending', submitted_at timestamptz DEFAULT now(), reviewed_at timestamptz);

CREATE TABLE IF NOT EXISTS required_courses (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid, project_id uuid, course_name text, required boolean DEFAULT true, added_by uuid, created_at timestamptz DEFAULT now());

CREATE TABLE IF NOT EXISTS positions (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), title text, created_by uuid, created_at timestamptz DEFAULT now());

ALTER TABLE projects ADD COLUMN IF NOT EXISTS created_by uuid;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS description text;
ALTER TABLE network_assets ADD COLUMN IF NOT EXISTS project_id uuid;
ALTER TABLE network_assets ADD COLUMN IF NOT EXISTS status text DEFAULT 'Pending';

INSERT INTO positions (title) VALUES ('Manager'),('Technician'),('Supervisor'),('Administrator'),('CEO'),('Field Supervisor'),('Project Manager'),('Lead Technician');