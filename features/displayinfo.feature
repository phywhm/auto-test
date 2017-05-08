# Created by xiama at 5/5/17
Feature: 各端申请实例时的播流信息
  # Enter feature description here

  Scenario: 使用PC端申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key            |      value        |
      | client_resolution |      1200x9000    |
      |  dpi              |       300         |
      |  os_type          |       1           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"300"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1200x9000"

  Scenario: 使用iPhone6Plus端申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key            |      value        |
      |   model   |   iPhone6Plus     |
      | os_type   |       4           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"401"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1080x1920"

  Scenario: 使用iPhone6端申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      |   model   |   iPhone6     |
      | os_type   |       4           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"326"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"750x1334"

  Scenario: 使用iPhone6端自带displayinfo申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      |   model   |   iPhone6     |
      | os_type   |       4           |
      |  dpi      |       300         |
      | resolution|      1200x9000    |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"326"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"750x1334"

  Scenario: 使用andriod端申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      | resolution|      1200x9000    |
      |  dpi      |       300         |
      | os_type   |       2           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"300"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1200x9000"

  Scenario: 使用web端申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      | resolution|      1200x9000    |
      |  dpi      |       300         |
      | os_type   |       3           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"300"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1200x9000"

  Scenario: 使用web端默认displayinfo申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      | os_type   |       3           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"320"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1920x1080"

  Scenario: 使用andriod端默认displayinfo申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key    |      value        |
      | os_type   |       2           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"320"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"1920x1080"

  Scenario: 使用PC端默认displayinfo申请一个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key            |      value        |
      |  os_type          |       1           |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"clientDisplayInfo/dpi"字段值应该是"-1"
    And paas收到的"apply"请求中"resolutionInfo/resolution"字段值应该是"-1x-1"