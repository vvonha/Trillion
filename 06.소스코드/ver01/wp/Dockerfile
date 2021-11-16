FROM wordpress:5.7.0

RUN mkdir -p /usr/src/blog
RUN mkdir -p /usr/src/blog/wp-content/plugins
RUN mkdir -p /usr/src/blog/wp-content/uploads
RUN cp -rf /usr/src/wordpress/* /usr/src/blog
RUN mv /usr/src/blog /usr/src/wordpress/
RUN chown -R www-data:www-data /usr/src/wordpress
RUN find /usr/src/wordpress/blog/ -type d -exec chmod 0755 {} \;
RUN find /usr/src/wordpress/blog/ -type f -exec chmod 644 {} \;
