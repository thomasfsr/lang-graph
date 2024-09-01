from graph import Workflow

wf = Workflow()

resp = wf.response("""Get 5 random lotto numbers""")

print(resp)