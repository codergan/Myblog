import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post,Category,Tag
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.views import View
from django.db.models import Q
class ContactView(View):
    def get(self, request):
        return render(request, 'blog/contact.html', {})

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please Enter the Keywords"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):

        #use get_context_data to get a dictionary from the parameter in model
        # get the dictionary and pass to context
        context = super().get_context_data(**kwargs)

        #  paginator、page_obj、is_paginated are inherited
        # paginator is an initialization of Paginator
        # page_obj is an initialization of Page
        # is_paginated is a bool parameter to determine whether the pagination is needed
        #use get to get the value from dictionary: context
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # Use pagination_data to get the data required
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # Note pagination_data returns a dictionary also
        context.update(pagination_data)

        # return the new context
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            #if no pagination, just return empty
            return {}


        left = []

        right = []

        left_has_more = False

        right_has_more = False

        first = False


        last = False

        # get the page required by user
        page_number = page.number

        #  get the total page number
        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number + 2]

            # if the rightmost and last page have page in between
            if right[-1] < total_pages - 1:
                right_has_more = True
            #show last page
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            #if request for the last page
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            # get two page num on left
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data
class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # Write get to raise the reading number
        # get returns a HttpResponse
        # after using get, you can have the self.object
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # reading num. +1
        self.object.increase_views()

        # view must return a HttpResponse
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # need the comment and the form
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
#def archives(request, year, month):
 #   post_list = Post.objects.filter(created_time__year=year,
 #                                   created_time__month=month
  #                                  ).order_by('-created_time')
   # return render(request, 'blog/index.html', context={'post_list': post_list})
class ArchievesView(ListView):
    model= Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        year= self.kwargs.get('year')
        month= self.kwargs.get('month')
        return super(ArchievesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)
class CategoryView(ListView):# can also inherit IndexView if you want
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
#def category(request, pk):
#    cate = get_object_or_404(Category, pk=pk)
#    post_list = Post.objects.filter(category=cate).order_by('-created_time')
#    return render(request, 'blog/index.html', context={'post_list': post_list})
class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

