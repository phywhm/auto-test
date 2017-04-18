# Created by xiama at 4/17/17
Feature: 申请实例




  Scenario: 一个用户默认可申请5个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Then the status of instance should be "0"

  @playing_time
  Scenario: 申请一个永久可玩的游戏
    Given 玩家通过租户"xiamatest"注册一个用户