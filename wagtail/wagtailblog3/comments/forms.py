from django import forms
from .models import BlogPageComment


class CommentForm(forms.ModelForm):
	"""评论表单，适应现有模型结构"""
	
	# 添加为非模型字段
	author_name = forms.CharField(max_length=100, required=False,
	                              widget=forms.TextInput(attrs={'placeholder': '您的名字', 'class': 'form-control'}))
	author_email = forms.EmailField(required=False,
	                                widget=forms.EmailInput(attrs={'placeholder': '您的邮箱', 'class': 'form-control'}))
	author_website = forms.URLField(required=False,
	                                widget=forms.URLInput(attrs={'placeholder': '您的网站', 'class': 'form-control'}))
	
	# 蜜罐字段，用于反垃圾
	honeypot = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'style': 'display:none !important'}),
		label="如果你能看到这个字段，请留空"
	)
	
	class Meta:
		model = BlogPageComment
		fields = ['content']  # 只包含模型中实际存在的字段
		widgets = {
			'content': forms.Textarea(attrs={
				'rows': 4,
				'placeholder': '请输入您的评论',
				'class': 'form-control'
			}),
		}
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.page = kwargs.pop('page', None)
		self.parent_id = kwargs.pop('parent_id', None)
		super().__init__(*args, **kwargs)
		
		# 已登录用户处理
		if self.user and self.user.is_authenticated:
			# 设置为非必填
			self.fields['author_name'].required = False
			self.fields['author_email'].required = False
			
			# 使用隐藏字段
			self.fields['author_name'].widget = forms.HiddenInput()
			self.fields['author_email'].widget = forms.HiddenInput()
			
			# 预填充用户信息
			if self.user.first_name or self.user.last_name:
				display_name = f"{self.user.first_name} {self.user.last_name}".strip()
				self.initial['author_name'] = display_name or self.user.username
			else:
				self.initial['author_name'] = self.user.username
			
			self.initial['author_email'] = self.user.email or ''
	
	def clean(self):
		"""验证表单数据"""
		cleaned_data = super().clean()
		
		# 检查蜜罐字段
		if cleaned_data.get('honeypot'):
			raise forms.ValidationError('检测到自动提交，请重试')
		
		return cleaned_data