![[icerik_politikaya_kadar_sorunsuz.mkv]] 

# Kullanmak için 
1. Sisteminizde Python ve Pip yüklü olduğuna emin olun.
2. Projeyi klonlayın ve proje klasörüne gidin.
3. python ile virtual environment oluşturun ve etkinleştirin.
	1. `python3 -m venv .venv`
	2. `source .venv/bin/activate`
4. 31. satırdaki `librewolf_path = "/usr/bin/firefox"` alanına kullacağınız tarayıcının çalıştırılabilir program yolunu giriniz.
5. 51. satırdaki `email_kutusu.send_keys("EMAIL")` bölümüne Bing sitesinde kullanacağınız mail adresinizi giriniz.
6.  61. satırdaki `parola_kutusu.send_keys("PASSWORD")` mail adresinizin parolasını yazın.
7. Eğer hesabınızda TOTP ile 2 Faktörlü doğrulama sistemi kullanıyorsanız;
	1. 84. satırdaki `totp_key = ""` çift tırnak içerisine anahtarınızı giriniz.
8. Hesabınızla ilk kez Bing'in sitesinde kullanıyorsanız bu projeyi çalıştırmadan önce siteye giderek "Kişisel hesapla oturum açın" seçeneğini seçin.
![[Ekran Görüntüsü - 2024-03-15 10-55-48.png]]
1. metinlerKlasor adındaki klasörün içerisine txt dosyalarınızı atın. 
	1. dosyaların SIRANUMARASI-DOSYAADI.txt şeklinde olması gereklidir. örnek: 
	2. ![[Ekran Görüntüsü - 2024-03-15 11-02-35.png]]
	3. txt dosyalarının içinde büyük harflerle yazılmış bir başlık olmalıdır. Bu başlık resimler oluşturulduktan sonra başlık adı ile aynı olan klasörün içine kopyalanacaktır.
	4. ![[Ekran Görüntüsü - 2024-03-15 11-05-21.png]]
2. 24. satırdaki tarayıcının indirme yolunu kendi sisteminizin indirme yolu ile değiştirin.
```python
librewolf_options.set_preference("browser.download.dir", "/home/aziz/İndirilenler/selenium_fotolar")  # İndirme dizini
```
1. 24. satırdaki yol ile 230. satıdaki `source_directory` nin aynı olması gereklidir.
2. 231. satırdaki `dest_directory` kendi sisteminize göre değiştirin.
```python
# Kaynak ve hedef dizinlerini belirle
source_directory = "/home/aziz/İndirilenler/selenium_fotolar"
dest_directory = "/home/aziz/Masaüstü/selenium_bing/sonuclar/"
```
1. projeyi çalıştırın.
	1. `python selenium_bing_imagecreator.py`