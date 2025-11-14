import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import csv
from LogikaKSZ import Dolgozo_KSZ_Osztaly, rendezes_ksz_fv


class Applikacio:
    def __init__(self, root_ablak):
        self.app = root_ablak
        self.app.title("KSZ Projekt - Adatrendező'")
        self.app.geometry("450x500")

        self.dolgozok_lista = []

        self.frame = ttk.Frame(self.app, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.lista_cim = ttk.Label(self.frame, text="Dolgozók:")
        self.lista_cim.pack()

        self.listbox = tk.Listbox(self.frame, height=10)
        self.listbox.pack(fill=tk.X, expand=True, pady=5)

        self.btn_frame = ttk.Frame(self.frame)
        self.btn_frame.pack(fill=tk.X)

        self.btn_rendez_nev = ttk.Button(self.btn_frame, text="Rendezés (Név)", command=self.rendez_nev)
        self.btn_rendez_nev.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_rendez_kor = ttk.Button(self.btn_frame, text="Rendezés (Kor)", command=self.rendez_kor)
        self.btn_rendez_kor.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_torles = ttk.Button(self.btn_frame, text="Törlés", command=self.torles_dolgozo)
        self.btn_torles.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.add_frame = ttk.LabelFrame(self.frame, text="Új dolgozó hozzáadása", padding="10")
        self.add_frame.pack(fill=tk.X, pady=10)

        self.nev_label = ttk.Label(self.add_frame, text="Név:")
        self.nev_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        self.nev_entry = ttk.Entry(self.add_frame, width=30)
        self.nev_entry.grid(row=0, column=1, padx=5, pady=2)

        self.kor_label = ttk.Label(self.add_frame, text="Kor:")
        self.kor_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        self.kor_entry = ttk.Entry(self.add_frame, width=30)
        self.kor_entry.grid(row=1, column=1, padx=5, pady=2)

        self.btn_hozzaad = ttk.Button(self.add_frame, text="Hozzáadás", command=self.hozzaad_dolgozo)
        self.btn_hozzaad.grid(row=2, column=0, columnspan=2, pady=5)

        self.menu = tk.Menu(self.app)
        self.app.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Fájl", menu=self.file_menu)
        self.file_menu.add_command(label="Adatok betöltése (CSV)", command=self.betolt_csv)
        self.file_menu.add_command(label="Adatok mentése (CSV)", command=self.ment_csv)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Kilépés", command=self.app.destroy)

        self.betolt_alap_adatok()
        self.frissit_lista()

        self.current_csv_file = None

    def betolt_alap_adatok(self):
        self.dolgozok_lista = \
        [
            Dolgozo_KSZ_Osztaly("Nagy János", 45),
            Dolgozo_KSZ_Osztaly("Kiss Mária", 28),
            Dolgozo_KSZ_Osztaly("Tóth Béla", 51),
            Dolgozo_KSZ_Osztaly("Szabó Elemér", 33)
        ]

    def frissit_lista(self):
        self.listbox.delete(0, tk.END)
        for dolgozo in self.dolgozok_lista:
            self.listbox.insert(tk.END, str(dolgozo))

    def rendez_nev(self):
        self.dolgozok_lista = rendezes_ksz_fv(self.dolgozok_lista, 'nev')
        self.frissit_lista()

    def rendez_kor(self):
        self.dolgozok_lista = rendezes_ksz_fv(self.dolgozok_lista, 'kor')
        self.frissit_lista()

    def torles_dolgozo(self):
        selected_index = self.listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Figyelmeztetés", "Kérem, válasszon ki egy dolgozót a törléshez!")
            return

        index = selected_index[0]
        torolt_dolgozo = self.dolgozok_lista[index]

        valasz = (messagebox.askyesno
        (
            "Törlés megerősítése",
            f"Biztosan törli: {torolt_dolgozo.nev} ({torolt_dolgozo.kor} év)?"
        ))

        if valasz:
            del self.dolgozok_lista[index]
            self.frissit_lista()

            if self.current_csv_file:
                self.auto_save_to_csv()

            messagebox.showinfo("Siker", f"{torolt_dolgozo.nev} sikeresen törölve!")

    def hozzaad_dolgozo(self):
        nev = self.nev_entry.get().strip()
        kor = self.kor_entry.get().strip()

        if not nev or not kor:
            messagebox.showwarning("Figyelmeztetés", "Kérem, adja meg a nevet és a kort!")
            return

        try:
            uj_dolgozo = Dolgozo_KSZ_Osztaly(nev, kor)
            self.dolgozok_lista.append(uj_dolgozo)
            self.frissit_lista()

            self.nev_entry.delete(0, tk.END)
            self.kor_entry.delete(0, tk.END)

            messagebox.showinfo("Siker", f"{nev} sikeresen hozzáadva!")
        except ValueError:
            messagebox.showerror("Hiba", "A kornak számnak kell lennie!")

    def betolt_csv(self):
        fajlnev = (filedialog.askopenfilename
        (
            title="CSV fájl megnyitása",
            filetypes=(("CSV fájlok", "*.csv"), ("Minden fájl", "*.*"))
        ))
        if not fajlnev:
            return

        encodings = ['utf-8', 'windows-1252', 'iso-8859-2', 'cp1250']

        for encoding in encodings:
            try:
                uj_lista = []
                with open(fajlnev, mode='r', encoding=encoding) as f:
                    csv_olvaso = csv.reader(f, delimiter=';')

                    try:
                        next(csv_olvaso, None)
                    except StopIteration:
                        pass

                    for sor in csv_olvaso:
                        if len(sor) == 2:
                            uj_lista.append(Dolgozo_KSZ_Osztaly(sor[0], sor[1]))

                if uj_lista:
                    self.dolgozok_lista = uj_lista
                    self.frissit_lista()
                    self.current_csv_file = fajlnev  # Track the loaded file
                    messagebox.showinfo("Siker", f"{len(uj_lista)} dolgozó betöltve a fájlból!")
                else:
                    messagebox.showwarning("Figyelmeztetés", "Nem található a programhoz megfelelő adat a fájlban!")
                return

            except UnicodeDecodeError:
                continue
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba a CSV olvasása közben: {e}")
                return

        messagebox.showerror("Hiba", "Nem sikerült beolvasni a fájlt. Próbálja meg UTF-8 kódolással menteni!")

    def ment_csv(self):
        fajlnev = (filedialog.asksaveasfilename
        (
            title="CSV fájl mentése",
            defaultextension=".csv",
            filetypes=(("CSV fájlok", "*.csv"), ("Minden fájl", "*.*"))
        ))

        if not fajlnev:
            return

        try:
            with open(fajlnev, mode='w', encoding='utf-8', newline='') as f:
                csv_iro = csv.writer(f, delimiter=';')

                csv_iro.writerow(["Nev", "Kor"])
                for dolgozo in self.dolgozok_lista:
                    csv_iro.writerow([dolgozo.nev, dolgozo.kor])

            messagebox.showinfo("Siker", f"Adatok sikeresen mentve: {fajlnev}")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba a CSV írása közben: {e}")

    def auto_save_to_csv(self):
        if not self.current_csv_file:
            return

        try:
            with open(self.current_csv_file, mode='w', encoding='utf-8', newline='') as f:
                csv_iro = csv.writer(f, delimiter=';')

                csv_iro.writerow(["Nev", "Kor"])
                for dolgozo in self.dolgozok_lista:
                    csv_iro.writerow([dolgozo.nev, dolgozo.kor])
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba az automatikus mentés közben: {e}")

    def mentsd_adatbazisba(self, eredeti_fajlnev):
        uj_fajlnev = eredeti_fajlnev.replace(".csv", "_mentes.csv")

        try:
            with open(uj_fajlnev, mode='w', encoding='utf-8', newline='') as f:
                csv_iro = csv.writer(f, delimiter=';')

                csv_iro.writerow(["Nev", "Kor"])
                for dolgozo in self.dolgozok_lista:
                    csv_iro.writerow([dolgozo.nev, dolgozo.kor])

            messagebox.showinfo("Automatikus mentés", f"Adatok automatikusan mentve: {uj_fajlnev}")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba az automatikus mentés közben: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Applikacio(root_ablak=root)
    root.mainloop()