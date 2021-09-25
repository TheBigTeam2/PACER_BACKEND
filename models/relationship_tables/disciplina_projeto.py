from sqlalchemy import Table, Column, ForeignKey
from models.Base import Base

disciplina_projeto = Table("disciplina_projeto",Base.metadata,
                     Column("dip_disciplina",ForeignKey("disciplina.dis_id")),
                     Column("dip_projeto",ForeignKey("projeto.pro_id"))
                     )