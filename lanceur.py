import subprocess

process = subprocess.Popen(
    ["python", "C:/Users/hello/Desktop/douchette/script.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
output, error = process.communicate()

if error:
    print(f"Erreur : {error.decode('utf-8')}")
else:
    print("Programme exécuté avec succès")
