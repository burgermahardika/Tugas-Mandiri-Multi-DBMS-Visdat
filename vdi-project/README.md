<div>
  <h2>Ringkasan Arsitektur</h2>
  <p>Sistem ini menggunakan arsitektur <strong>Multi-DBMS</strong> yang memisahkan penyimpanan data master dan transaksional:</p>
  <ul>
    <li><strong>DBMS 1 (Lokal):</strong> SQLite (<code>coffee_local.db</code>) — Berfungsi untuk menyimpan dan mengelola data master produk menu kopi.</li>
    <li><strong>DBMS 2 (Cloud):</strong> PostgreSQL / Supabase (via Transaction Pooler port 6543) — Berfungsi untuk menyimpan data transaksi penjualan dan informasi cabang toko.</li>
  </ul>

  <h2>Alur Integrasi (Data Pipeline)</h2>
  <p>Proses penyatuan data dilakukan secara terstruktur menggunakan pustaka <strong>Pandas</strong>:</p>
  <ul>
    <li>Data master produk diambil dari database lokal SQLite menggunakan konektor SQLAlchemy.</li>
    <li>Data transaksi penjualan diambil secara <em>real-time</em> dari cloud database PostgreSQL Supabase.</li>
    <li>Kedua sumber data digabungkan secara <em>in-memory</em> menggunakan Pandas untuk membentuk satu dataset analitik yang utuh dan siap divisualisasikan.</li>
  </ul>

  <h2>Fitur Interaktivitas Antarmuka Visualisasi</h2>
  <p>Antarmuka web interaktif yang dibangun menyediakan beberapa fitur utama:</p>
  <ul>
    <li><strong>Panel Filter & Kontrol Data Interaktif:</strong> Memungkinkan pengguna menyaring cakupan data penjualan berdasarkan cabang toko dan metode pembayaran secara dinamis melalui panel ekspander utama.</li>
    <li><strong>Metrik Ringkasan Real-Time:</strong> Menampilkan kartu metrik utama (Total Pendapatan, Volume Terjual, dan Jumlah Transaksi) yang otomatis memperbarui nilai kalkulasi berdasarkan filter yang dipilih.</li>
    <li><strong>Visualisasi Grafik & Tabel Dinamis:</strong> Menyajikan tata letak berbasis <em>tabs</em> yang mencakup grafik batang vertikal/horizontal berbasis Plotly, diagram lingkaran distribusi pembayaran, serta tabel data interaktif.</li>
  </ul>
</div>
