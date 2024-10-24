import sqlalchemy as sa
import sqlalchemy.orm as sao

engine = sa.create_engine("sqlite+pysqlite:///:memory:")
Session = sao.sessionmaker()
Base = sao.declarative_base()

class Task(Base):
    __tablename__ = "task"
    
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True)
    titulo: sao.Mapped[str] = sao.mapped_column(sa.String(30))
    descripcion: sao.Mapped[str] = sao.mapped_column(sa.String(30))
    #fecha_vencimiento: sao.Mapped[str] = sao.mapped_column(sa.DateTime)
    fecha_vencimiento: sao.Mapped[str] = sao.mapped_column(sa.String(30))
    prioridad: sao.Mapped[str] = sao.mapped_column(sa.String(30))
    categoria: sao.Mapped[str] = sao.mapped_column(sa.String(30))
    completada: sao.Mapped[str] = sao.mapped_column(sa.Boolean)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, titulo={self.titulo!r}, descripcion={self.descripcion!r}, fecha_vencimiento={self.fecha_vencimiento!r}, prioridad={self.prioridad!r}, categoria={self.categoria!r}, completada={self.completada!r} )"


Base.metadata.create_all(engine)


def insert_task(task):
    with sao.Session(engine) as session:
        new_task = Task(titulo=task['titulo'], descripcion=task['descripcion'], fecha_vencimiento=task['fecha_vencimiento'], prioridad=task['prioridad'], categoria=task['categoria'], completada=False)
        session.add(new_task)

        session.commit()

def select_task():
    task_list = []

    with sao.Session(engine) as session:
        query = sa.select(Task)

        for task in session.scalars(query):
            task_list.append(task)

        return task_list
    
def delete_task(task_id):
    with sao.Session(engine) as session:
        del_task = session.get(Task, task_id)
        session.delete(del_task)
        session.commit()

def change_completed_task(task_id, value):
    with sao.Session(engine) as session:
        upd_task = session.get(Task, task_id)
        upd_task.completada = value
        session.commit()

def update_task(task_id, updated_task):
    with sao.Session(engine) as session:
        upd_task = session.get(Task, task_id)

        if 'titulo' in updated_task:
            upd_task.titulo = updated_task['titulo']
        if 'descripcion' in updated_task:
            upd_task.descripcion = updated_task['descripcion']
        if 'fecha_vencimiento' in updated_task:
            upd_task.fecha_vencimiento = updated_task['fecha_vencimiento']
        if 'prioridad' in updated_task:
            upd_task.prioridad = updated_task['prioridad']
        if 'categoria' in updated_task:
            upd_task.categoria = updated_task['categoria']
        session.commit()