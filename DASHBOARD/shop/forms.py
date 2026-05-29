from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nama_produk', 'kategori', 'deskripsi', 'harga', 'stok', 'gambar']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'placeholder': 'Contoh: Parfum Linen Spray'}),
            'kategori': forms.TextInput(attrs={'placeholder': 'Contoh: Rumah Tangga'}),
            'deskripsi': forms.Textarea(attrs={'placeholder': 'Tulis deskripsi produk', 'rows': 5}),
            'harga': forms.NumberInput(attrs={'placeholder': '28900'}),
            'stok': forms.NumberInput(attrs={'placeholder': '100'}),
            'gambar': forms.ClearableFileInput(),
        }
