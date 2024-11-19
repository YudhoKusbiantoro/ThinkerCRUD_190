import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
# Impor pustaka yang dibutuhkan
#import sqlite3
#from tkinter import Tk
#from tkinter import Label
#from tkinter import Entry
#from tkinter import Button
#from tkinter import StringVar
#from tkinter import messagebox
#from tkinter import ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuat koneksi ke database SQLite
    cursor = conn.cursor() # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''') # Membuat tabel jika belum ada
    conn.commit() # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database

def fetch_data(): #digunakan untuk mengambil semua data dari tabel nilai_siswa dalam database SQLite (nilai_siswa.db).
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database SQLite
    cursor = conn.cursor()  # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute("SELECT * FROM nilai_siswa")  # Membuat cursor untuk menjalankan perintah SQL
    rows = cursor.fetchall()  # Mengambil semua baris hasil query dalam bentuk list of tuples
    conn.close()  # Menutup koneksi database
    return rows  # Mengembalikan data hasil query

def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database SQLite
    cursor = conn.cursor() # Membuat cursor untuk menjalankan perintah SQL
     # Menjalankan perintah SQL untuk menyimpan data baru
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database
#digunakan untuk menyimpan data baru ke dalam tabel nilai_siswa di database SQLite.
def update_database(record_id, nama, biologi, fisika, inggris, prediksi): 
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database SQLite
    cursor = conn.cursor() # Membuat cursor untuk menjalankan perintah SQL
     # Menjalankan perintah SQL untuk menyimpan data baru
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()   # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

def delete_database(record_id): #digunakan untuk menghapus data tertentu dari tabel nilai_siswa di database SQLite berdasarkan ID record
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database SQLite
    cursor = conn.cursor() # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))# Menjalankan perintah SQL untuk menghapus data berdasarkan ID
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database


 # ini berguna untuk memberikan prediksi fakultas berdasarkan perbandingan nilai antara tiga mata pelajaran
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:#Jika nilai Biologi lebih tinggi dari Fisika dan Inggris, 
        return "Kedokteran" #maka prediksi fakultas adalah Kedokteran.
    elif fisika > biologi and fisika > inggris: #Jika nilai Fisika lebih tinggi,
        return "Teknik" #maka prediksi fakultas adalah Teknik.
    elif inggris > biologi and inggris > fisika: #Jika nilai Inggris lebih tinggi,
        return "Bahasa" #maka prediksi fakultas adalah Bahasa.
    else: #Jika tidak ada nilai yang lebih tinggi (misalnya ada dua nilai yang sama),
        return "Tidak Diketahui" #maka fungsi akan mengembalikan prediksi "Tidak Diketahui".


def submit(): #untuk memproses dan menyimpan input pengguna dalam aplikasi berbasis GUI.
    try:
        nama = nama_var.get() # # Mengambil input dari field yang ada
        biologi = int(biologi_var.get()) # Mengonversi input Biologi ke integer
        fisika = int(fisika_var.get()) # Mengonversi input Fisika ke integer
        inggris = int(inggris_var.get()) # Mengonversi input Inggris ke integer

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")
            #  Validasi untuk memastikan nama tidak kosong
        prediksi = calculate_prediction(biologi, fisika, inggris)   # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)   # Menyimpan data ke database

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
         # Membersihkan input dan memperbarui tabel
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")
        # Menangani jika input tidak valid (contoh: pengguna memasukkan data yang bukan angka atau nama kosong)



#pengguna untuk memperbarui data siswa yang sudah ada di database,
#dengan memperhitungkan nilai baru yang dimasukkan dan menghitung kembali prediksi 
def update(): 
    try:
        if not selected_record_id.get():  # Memastikan pengguna memilih data untuk diupdate
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
          # Mengambil nilai baru dari input
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  # Validasi jika nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

         # Menghitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") # Menampilkan pesan sukses
        clear_inputs()    # Membersihkan input dan memperbarui tabel
        populate_table()
           # Menangani jika input tidak valid
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete(): # memungkinkan pengguna untuk menghapus data siswa yang sudah ada dalam database.
    try:
        if not selected_record_id.get():    # Memastikan pengguna memilih data untuk dihapus
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get()) # Mengambil ID record yang dipilih
        delete_database(record_id) # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!") # Menampilkan pesan sukses
        # Membersihkan input dan memperbarui tabel
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
         # Menangani jika input tidak valid


# digunakan untuk membersihkan semua input pada form. 
# Ketika fungsi ini dipanggil, semua nilai pada input form 
# akan di-set ke string kosong ("").
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")


#digunakan untuk memperbarui tampilan tabel 
# di GUI dengan data terbaru dari database.
def populate_table():
    for row in tree.get_children():#Menghapus semua baris yang ada di dalam tabel sebelum memperbarui tampilan
        tree.delete(row)#tree di sini adalah objek Treeview yang digunakan untuk menampilkan data.
    for row in fetch_data():# Fungsi fetch_data() akan mengambil semua data dari database
        tree.insert('', 'end', values=row) #kemudian setiap baris data dimasukkan ke dalam tabel menggunakan tree.insert().

def fill_inputs_from_table(event): #Fungsi ini digunakan untuk mengisi form input dengan data yang dipilih dari tabel.
    try:
        selected_item = tree.selection()[0]#Mengambil ID dari baris yang dipilih di tabel. 
        selected_row = tree.item(selected_item)['values']#Mengambil nilai dari baris yang dipilih. 
        #Nilai-nilai ini berupa tuple yang berisi data dari kolom tabel.

        selected_record_id.set(selected_row[0])#Mengisi ID record yang dipilih ke dalam variabel
        nama_var.set(selected_row[1])     #Mengisi nama siswa ke field input nama.
        biologi_var.set(selected_row[2])  #Mengisi nilai Biologi ke field input Biologi.
        fisika_var.set(selected_row[3])   #Mengisi nilai Fisika ke field input Fisika.
        inggris_var.set(selected_row[4])  #Mengisi nilai Inggris ke field input Inggris.
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Label dan entry untuk input data siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#Membuat Tombol (Button) untuk Operasi: Add, Update, Delete
Button(root, text="Add", command=submit, bg="lightgreen", fg="black").grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update, bg="lightblue", fg="black").grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete, bg="lightcoral", fg="black").grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize()) # Menambahkan judul kolom
    tree.column(col, anchor='center')   # Mengatur teks agar berada di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)# Menghubungkan tabel dengan event klik untuk mengisi form input

populate_table()# Mengisi tabel dengan data yang ada di database

root.mainloop()# Menjalankan aplikasi GUI