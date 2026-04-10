
from django import forms
from .models import Product, Category

class ProductAdminForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),
        required=False,
        label="Category",
        help_text="Select a main category to filter subcategories."
    )
    
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = "Sub Category"
        self.fields['category'].required = False
        
        if self.instance and self.instance.pk and self.instance.category:
            if self.instance.category.parent:
                self.fields['parent_category'].initial = self.instance.category.parent
                self.fields['category'].queryset = Category.objects.filter(parent=self.instance.category.parent)
            else:
                self.fields['parent_category'].initial = self.instance.category
                self.fields['category'].queryset = Category.objects.filter(parent=self.instance.category)
        else:
            self.fields['category'].queryset = Category.objects.none()
