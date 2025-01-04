from django.db import models
from django.utils import timezone
import os
import uuid
from django.contrib.auth.models import User

def item_based_path(instance, filename):
    category_id = instance.category.id
    extension = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"
    return os.path.join(f'clothing_items/category_{category_id}', unique_name)

class Gender(models.TextChoices):
    MALE = 'M', 'Чоловічий' 
    FEMALE = 'F', 'Жіночий'

class Collection(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField( max_length=1, choices=Gender.choices + (('U', 'Унісекс'),), default='U')
    show_on_site = models.BooleanField(default=False)  # Відображати користувачам

class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    show_on_site = models.BooleanField(default=False)  # Відображати користувачам

class Tag(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='clothing_items', on_delete=models.CASCADE)
    
class ClothingItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    is_discount_active = models.BooleanField(default=True)
    catalog_photo = models.ImageField(upload_to=item_based_path, null=True, blank=True)  # Фото для каталогу
    catalog_hover_photo = models.ImageField(upload_to=item_based_path, null=True, blank=True)  # Фото при наведенні
    collection = models.ForeignKey(Collection, related_name='clothing_items', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='clothing_items', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='clothing_items', blank=True)
    gender = models.CharField( max_length=1, choices=Gender.choices)
    show_on_site = models.BooleanField(default=True)  # Відображати користувачам
    available = models.BooleanField(default=True)  # Наявність
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    available_quantity = models.PositiveIntegerField()  # Доступна кількість


    def save(self, *args, **kwargs):
        # Перевірка наявності
        if self.available_quantity <= 0:
            self.available = False
        else:
            self.available = True
   
        # Перевірка знижки

        if not self.is_discount_active:
            # Якщо знижка вимкнена вручну, просто збережемо ціну без знижки
            self.final_price = self.price
        else:
            # Якщо знижка активна, перевіряємо, чи діє вона за датами
            now = timezone.now()
            if self.discount_start and self.discount_end:
                # Якщо поточний час знаходиться в межах дат знижки, знижка активна
                if self.discount_start <= now <= self.discount_end:
                    self.final_price = self.price * (1 - self.discount_percentage / 100)
                else:
                    self.final_price = self.price  # Знижка не активна поза межами дат
            elif self.discount_start and now >= self.discount_start:
                # Якщо знижка має тільки дату початку і зараз після цієї дати
                self.final_price = self.price * (1 - self.discount_percentage / 100)
            elif self.discount_end and now <= self.discount_end:
                # Якщо знижка має тільки дату закінчення і зараз до цієї дати
                self.final_price = self.price * (1 - self.discount_percentage / 100)
            else:
                # Якщо знижка неактивна
                self.final_price = self.price

        super().save(*args, **kwargs)

    def get_price_for_user(self):
        return self.final_price

    def __str__(self):
        return self.name

# Склад
class MaterialComposition(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='material_compositions', on_delete=models.CASCADE)
    material_name = models.CharField(max_length=200)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  

    def __str__(self):
        return f"{self.material_name}: {self.percentage}%"
    
# Розміри

class ClothingTopSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='clothing_top_sizes', on_delete=models.CASCADE)
    size_name = models.CharField(max_length=5, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L')])

    def __str__(self):
        return f"Top Size: {self.size_name}"
    
class ClothingBottomSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='clothing_bottom_sizes', on_delete=models.CASCADE)
    size_name = models.CharField(max_length=5, choices=[('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'),
                                                        ('40', '40'), ('42', '42'), ('44', '44'), ('46', '46')])

    def __str__(self):
        return f"Bottom Size: {self.size_name}"
    
class FootwearSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='footwear_sizes', on_delete=models.CASCADE)
    size_name = models.CharField(max_length=5, choices=[('35', '35'),('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'),
                                                        ('40', '40'), ('41', '41'), ('42', '42')])

    def __str__(self):
        return f"Footwear Size: {self.size_name}"

# Колір
class ItemColor(models.Model):
    name = models.CharField(max_length=150)  
    rgb_value = models.CharField(max_length=15)
    clothing_item = models.ForeignKey(ClothingItem, related_name='clothing_color', on_delete=models.CASCADE)

class ItemPhoto(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='clothing_photo', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=item_based_path)
    def __str__(self):
        return f"Image for {self.announcement.title}"

    def delete(self, *args, **kwargs):
        # Перевірка, чи файл фізично існує, і його видалення
        if self.image and self.image.storage.exists(self.image.name):
            self.image.delete()
        super().delete(*args, **kwargs)

class Like(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.clothing_item.name}"
    
    class Meta:
        unique_together = ('clothing_item', 'user') 

