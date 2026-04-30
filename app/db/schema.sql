-- Vectorless RAG Database Schema for Supabase
-- This schema creates tables and functions for document storage and semantic search

-- Enable required extensions
create extension if not exists pgcrypto;

create table documents (
    id uuid primary key default gen_random_uuid(),
    file_name text,
    page_number int,
    chunk_text text,
    created_at timestamp default now(),
    tsv tsvector
);

create index idx_docs_search
on documents using gin(tsv);

create function update_tsv()
returns trigger as $$
begin
new.tsv := to_tsvector(
'english',
coalesce(new.chunk_text,'')
);
return new;
end
$$ language plpgsql;

create trigger trg_docs
before insert or update
on documents
for each row execute function update_tsv();

create or replace function search_docs(
search_query text,
match_count int
)
returns table(
file_name text,
page_number int,
chunk_text text
)
language sql
as $$
select file_name, page_number, chunk_text
from documents
where tsv @@ plainto_tsquery(search_query)
order by ts_rank(tsv, plainto_tsquery(search_query)) desc
limit match_count;
$$;