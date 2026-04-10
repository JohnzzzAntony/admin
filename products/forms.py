from django import forms
from .models import Product, Category

class ProductAdminForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),
        required=False,
        label="Category",
        help_text="Select a main category to filter subcategories."
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Sub Category"
    )
    
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = "Sub Category"
        self.fields['category'].required = False
        
        # Always allow all categories for validation to pass after AJAX selection
        self.fields['category'].queryset = Category.objects.all()
        
        # Explicit IDs for JavaScript reliability
        self.fields['category'].widget.attrs['id'] = 'id_category'
        self.fields['parent_category'].widget.attrs['id'] = 'id_parent_category'
        
        if self.instance and self.instance.pk and self.instance.category:
            if self.instance.category.parent:
                self.fields['parent_category'].initial = self.instance.category.parent
            else:
                self.fields['parent_category'].initial = self.instance.category

    def clean(self):
        cleaned_data = super().clean()
        parent_cat = cleaned_data.get('parent_category')
        sub_cat = cleaned_data.get('category')
        
        # Priority Logic:
        # 1. If sub_cat is selected, use it.
        # 2. If no sub_cat but parent_cat is selected, use parent_cat.
        if parent_cat and not sub_cat:
            cleaned_data['category'] = parent_cat
            
        return cleaned_data
