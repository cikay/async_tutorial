
Bu projenin çalışması için önce bilgisayarınıza [poetry](https://python-poetry.org/) ve python 3.11.5 kurulması gerekiyor.

Aşağıdaki komutla environment kurulur ve aktif edilir.

```
poetry shell
```

Aşağıdaki komutla paketler indirilir.

```
poetry install
```

Aşağıdaki komutla proje çalıştırılır

```
uvicorn main:app --reload
```

`http://127.0.0.1:8000/docs` adresine gidilir ve send_message endpointine istek atılır.

Istek atılırken dikkat edilmesi gerekler:

1. Token bilgisi kullanıcı adının tersten yazılmış şekilde olmalı
2. group id'si 1 olmalı
3. message 40 kelimeden daha kısa olmalı

Note: Sadece gruptaki kullanıcılar mesaj atınca mesaj diğelerine gönderilir, simulasyon yapılır.

Gruptaki kullanıcılar: ayşe, fatma, mehmet, ali

Kod değiştirip çalıştırılması öğrenmeye katkı sağlar.
