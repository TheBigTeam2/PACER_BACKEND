from sqlalchemy import Table, Column, ForeignKey
from models.Base import Base

projeto_equipe = Table("projeto_equipe",Base.metadata,
                 Column("pre_projeto",ForeignKey("projeto.pro_id")),
                 Column("pre_equipe",ForeignKey("equipe.equ_id"))
)