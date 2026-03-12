import speech_recognition as sr
import os
from supabase import create_client

# --- CONFIGURAZIONE ---
URL_SUPABASE = "https://csrsqjteiouzdjrwxezw.supabase.co"
KEY_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzcnNxanRlaW91emRqcnd4ZXp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIyMDAyOTUsImV4cCI6MjA4Nzc3NjI5NX0.Xcmb74FlkJfaE-rBNV5E-kG4pz5a-libx_Ygi9n9FcY"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

def parla(testo):
    """Fa parlare il Mac"""
    print(f"🤖 Jarvis: {testo}")
    # Usa la voce di sistema del Mac (Alice è un'ottima voce italiana)
    os.system(f"say -v Alice '{testo}'")

def esegui_azione(comando):
    """Analizza il testo e decide cosa fare senza attivazione manuale"""
    t = comando.lower()
    
    if "apri" in t:
        app = t.split("apri")[-1].strip()
        parla(f"Certamente, apro {app}")
        os.system(f"open -a '{app}'")
        return True

    elif "volume" in t:
        if "alza" in t or "su" in t:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 15)'")
            parla("Volume alzato")
        elif "abbassa" in t or "giù" in t:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 15)'")
            parla("Volume abbassato")
        return True

    elif "chiudi" in t:
        app = t.split("chiudi")[-1].strip()
        parla(f"Chiudo {app}")
        os.system(f"osascript -e 'quit app \"{app}\"'")
        return True

    return False

def ascolta_infinito():
    r = sr.Recognizer()
    # Ottimizzazione per non bloccarsi sui rumori di fondo
    r.energy_threshold = 300 
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        parla("Sistema vocale online. Sono in ascolto.")
        
        while True:
            try:
                # Ascolta in background
                audio = r.listen(source, phrase_time_limit=4)
                testo = r.recognize_google(audio, language="it-IT").lower()
                print(f"👂 Sentito: {testo}")

                # Prova a eseguire l'azione direttamente dal testo sentito
                esegui_azione(testo)
                        
            except sr.UnknownValueError:
                # Non ha capito, ma continua a girare senza errori
                pass
            except Exception as e:
                # Se c'è un errore di connessione, riprova dopo un secondo
                print(f"🔄 Riconnessione... {e}")

if __name__ == "__main__":
    ascolta_infinito()