FROM alpine:latest
RUN apk update && apk add --no-cache tor cmatrix curl bash net-tools python3
ENV TERM=xterm-256color
CMD ["sh"]
