# Created by xiama at 5/4/17
Feature: saas server的配置
  # Enter feature description here

  @playing_time
  Scenario: 当单次播流时长大于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"globalPlayingTime"配置值为"60000"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 最后一个请求的状态应该是"InService"
    When 等待"45000"毫秒
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"15000"毫秒
    Then 这个请求的状态应该是"Finished"
    And 这个实例应该收到"timeover"消息
    And 接入商"xiamatest"已占用的实例个数应该为"500"

  @playing_time
  Scenario: 当单次播流时等于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"globalPlayingTime"配置值为"60000"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  60000  |
    Then 最后一个请求的状态应该是"InService"
    When 等待"45000"毫秒
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"15000"毫秒
    Then 这个请求的状态应该是"Finished"
    And 这个实例应该收到"timeover"消息
    And 接入商"xiamatest"已占用的实例个数应该为"500"

  @playing_time
  Scenario: 当单次播流时小于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"globalPlayingTime"配置值为"60000"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  40000  |
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"30000"毫秒
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"10000"毫秒
    Then 这个请求的状态应该是"Finished"
    And 这个实例应该收到"timeover"消息
    And 接入商"xiamatest"已占用的实例个数应该为"500"

  @playing_time
  Scenario: 当单次播流时长是字符串时, 申请实例
  "set the global playing time to '12312sf'"
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"globalPlayingTime"配置值为"6s0000"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  40000  |
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"30000"毫秒
    Then 最后一个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"10000"毫秒
    Then 这个请求的状态应该是"Finished"
    And 这个实例应该收到"timeover"消息
    And 接入商"xiamatest"已占用的实例个数应该为"500"


  @no_impl
  Scenario: 单用户可申请5个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    Given 用户申请一个"random"实例
    Given 用户申请一个"random"实例
    Given 用户申请一个"random"实例
    Given 用户申请一个"random"实例
    When 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"505"


  @no_impl
  Scenario: 修改单用户可申请实例个数
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"cid_max_ct"配置值为"2"
    Given 用户申请一个"random"实例
    Given 用户申请一个"random"实例
    When 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"502"


  @no_impl
  Scenario: 一个用户只能打开一个同款游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    When 等待"1000"毫秒
    Given 用户申请一个实例
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"501"

  @no_impl
  Scenario: 修改单用户同一游戏实例个数
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"package_max_count"配置值为"2"
    Given 用户申请一个实例
    Given 用户申请一个实例
    When 等待"1000"毫秒
    Given 用户申请一个实例
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"502"


  Scenario: 默认的时间提醒和倒计时
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"InService"
    And 这个请求的"address"消息中"countdownTime"字段值应该是"60000"
    And 这个请求的"address"消息中"remindTime"字段值应该是"300000"

  Scenario Outline: 修改时间提醒和倒计时
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"<key>"配置值为"<value>"
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"InService"
    And 这个请求的"address"消息中"<result_key>"字段值应该是"<value>"
    Examples:
      | key  |  result_key |  value  |
      | playing_countdown_time | countdownTime | 40000 |
      | playing_remind_time | remindTime | 300001 |

  Scenario: 修改最大排队人数
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    And 设置接入商"xiamatest"的"wait_max_count"配置值为"1"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个路由为"3,4"的实例
    When 等待"1000"毫秒
    Then 用户申请一个路由为"3,4"的实例
    Then 最后一个请求的状态应该是"Finished"
    Given 用户申请一个实例
    When 等待"1000"毫秒
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"Finished"

  Scenario: 显示排队预估时间
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    And 设置接入商"xiamatest"的"showEstimateTime"配置值为"True"
    Given 用户申请一个实例
    When 等待"1000"毫秒
    Then 最后一个请求的状态应该是"Enqueue"

    And 这个请求的"waiting"消息中"countdownTime"字段值应该是"60000"


  Scenario: 修改无操作超时时长
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"noInputTime"配置值为"601010"
    When 开始记录paas收到的请求
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"noInputTime"字段值应该是"601010"


  Scenario: 默认的configinfo和cidinfo的保存路径
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"cidInfo/path"字段值应该是"/sdcard/hmcp-apkinfos/%s-cid"
    And paas收到的"apply"请求中"configInfo/path"字段值应该是"/sdcard/hmcp-apkinfos/%s.info"


  Scenario Outline: 修改configinfo和cidinfo的保存路径
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置接入商"xiamatest"的"<key>"配置值为"<value>"
    When 开始记录paas收到的请求
    Given 用户申请一个实例
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    When 等待"100000"毫秒
    And paas收到的"apply"请求中"<result_key>"字段值应该是"<value>"
    Examples:
      | key  |  result_key |  value  |
      | paas_cidInfo_path | cidInfo/path | /test |
      | paas_configInfo_path | configInfo/path | /test2 |