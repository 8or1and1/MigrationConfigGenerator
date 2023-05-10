from interfaces.begin_frame import BeginFrame
from db_tools.db_worker import db_worker

backend = db_worker()

main_frame = BeginFrame(backend, True)
main_frame.root.mainloop()