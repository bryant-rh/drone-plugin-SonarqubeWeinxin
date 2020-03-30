sonarscan 扫描结果企业微信通知

#sonar-scan扫描结果通知企业微信
- name: sonar_notify_weixin
  image: harbor.cechealth.cn/drone-plugin/drone-sonarwexin:0.1
  pull: always
  #environment:
  #  corpid:
  #    from_secret: wechat_corpid
  #  corp_secret:
  #    from_secret: wechat_corp_secret_approval
  settings:
    corpid: ww55f9d11848308ad5
    corp_secret: qAa8hrycB0erzO1BQ0dpcg0BUqIf2rAf8rvZRwB9v7A
    agent_id: '1000003'
    sonar_url: 'http://sonarqube.cechealth.cn'
    to_user: '@all'
  #commands:
  #  - cat /drone/src/.scannerwork/report-task.txt
  when:
    branch:
      - master

