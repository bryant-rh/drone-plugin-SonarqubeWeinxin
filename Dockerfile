FROM harbor.cechealth.cn/tools/python:2.7.16-alpine
ADD SonarqubeWeixin.py /bin
RUN chmod +x /bin/SonarqubeWeixin.py
#ENTRYPOINT ["python","/bin/weixin.py"]
#ENTRYPOINT ["python","/bin/weixin.py"]
CMD ["python","/bin/SonarqubeWeixin.py"]
#CMD ["/bin/sh"]

