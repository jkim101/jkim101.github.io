---
layout: single
title: Debug Posts
permalink: /debug/
---

# All Posts

<ul>
{% for post in site.posts %}
  <li>{{ post.date | date: "%Y-%m-%d" }} - {{ post.title }} (Hidden: {{ post.hidden }})</li>
{% endfor %}
</ul>
