from sqlalchemy import Table, Column, ForeignKey
from models.Base import Base

aluno_equipe = Table("aluno_equipe",Base.metadata,
    Column("ale_aluno",ForeignKey("aluno.alu_ra")),
    Column("ale_equipe",ForeignKey("equipe.equ_id"))
)