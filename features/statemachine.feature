# Created by xiama at 4/6/17
Feature: state machine testing
  # Enter feature description here

  @smoke
  Scenario Outline: test the Created status
    Given 用户创建一个 "Created" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |         Linked           |
      |  AccessLinkFailed                  |        Finished          |
      |  SyncApplyInstanceSuccess          |         Created          |
      |  SyncApplyInstanceNoIdle           |         Created          |
      |  SyncApplyInstanceRpcException     |         Created          |
      |  SyncApplyInstanceRetry            |         Created          |
      |  SyncApplyInstanceRetryOut         |         Created          |
      |  SyncApplyInstanceError            |         Created          |
      |  AsyncInstancePreparationSuccess   |         Created          |
      |  AsyncInstancePreparationFailed    |         Created          |
      |  CloudServiceApply                 |         Created          |
      |  CloudServiceTimeout               |         Created          |
      |  CloudUserExit                     |        Finished          |
      |  AccessLinkClientDisconnectTimeout |         Created          |
      |  AccessLinkServerDisconnect        |         Created          |
      |  InstanceNoInputTimeout            |         Created          |
      |  InstanceError                     |         Created          |
      |  InstanceReleaseSuccess            |         Created          |
      |  InstanceReleaseFailed             |         Created          |
      |  InstanceReleaseRetry              |         Created          |
      |  InstanceReleaseRetryOut           |         Created          |
      |  CloudUserEnqueueConfirmYes        |         Created          |
      |  CloudUserDequeue                  |         Created          |
      |  CloudUserEnqueue                  |         Created          |
      |     DoRefreshStoken                |         Created          |
      |    DoRefreshStokenSuccess          |         Created          |
      |    DoRefreshStokenFailed           |         Created          |
      |      DoChangeResolution            |         Created          |
      |  DoChangeResolutionSuccess         |         Created          |
      |   DoChangeResolutionFailed         |         Created          |



  Scenario Outline: test the Linked status
    Given 用户创建一个 "Linked" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |         Linked           |
      |  AccessLinkFailed                  |         Linked           |
      |  SyncApplyInstanceSuccess          |         Linked           |
      |  SyncApplyInstanceNoIdle           |         Linked           |
      |  SyncApplyInstanceRpcException     |         Linked           |
      |  SyncApplyInstanceRetry            |         Linked           |
      |  SyncApplyInstanceRetryOut         |         Linked           |
      |  SyncApplyInstanceError            |         Linked           |
      |  AsyncInstancePreparationSuccess   |         Linked           |
      |  AsyncInstancePreparationFailed    |         Linked           |
      |  CloudServiceApply                 |        InService         |
      |  CloudServiceTimeout               |         Linked           |
      |  CloudUserExit                     |        Finished          |
      |  AccessLinkClientDisconnectTimeout |        Finished          |
      |  AccessLinkServerDisconnect        |        Finished          |
      |  InstanceNoInputTimeout            |         Linked           |
      |  InstanceError                     |         Linked           |
      |  InstanceReleaseSuccess            |         Linked           |
      |  InstanceReleaseFailed             |         Linked           |
      |  InstanceReleaseRetry              |         Linked           |
      |  InstanceReleaseRetryOut           |         Linked           |
      |  CloudUserEnqueueConfirmYes        |         Linked           |
      |  CloudUserDequeue                  |         Linked           |
      |  CloudUserEnqueue                  |         Linked           |
      |     DoRefreshStoken                |         Linked           |
      |    DoRefreshStokenSuccess          |         Linked           |
      |    DoRefreshStokenFailed           |         Linked           |
      |      DoChangeResolution            |         Linked           |
      |  DoChangeResolutionSuccess         |         Linked           |
      |   DoChangeResolutionFailed         |         Linked           |


  @no-impl
  Scenario Outline: test the Linked status with queue status
    Given 用户创建一个 "Linked" 的状态机
    When I set the status of product to "<islimit>"
    And 设置paas不返回回调地址
    When I set the size of queue to "<queue_size>"
    When 用户触发"CloudServiceApply"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |  islimit  |  queue_size  |         status        |
      |    over   |      2       | WaitingConfirmEnqueue |
      |  notover  |      3       | WaitingConfirmEnqueue |
      |    over   |      0       | WaitingConfirmEnqueue |
      |  notover  |      0       |    InstanceApplying   |


  Scenario Outline: test the InstanceApplying status
    Given 用户创建一个 "InstanceApplying" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |   InstanceApplying       |
      |  AccessLinkFailed                  |   InstanceApplying       |
      |  SyncApplyInstanceSuccess          |      InService           |
      |  SyncApplyInstanceNoIdle           |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceRpcException     |      InService           |
      |  SyncApplyInstanceRetry            |      InService           |
      |  SyncApplyInstanceRetryOut         |       Finished           |
      |  SyncApplyInstanceError            |       Finished           |
      |  AsyncInstancePreparationSuccess   |       InService          |
      |  AsyncInstancePreparationFailed    |    InstanceReleaseing    |
      |  CloudServiceApply                 |    InstanceApplying      |
      |  CloudServiceTimeout               |    InstanceApplying      |
      |  CloudUserExit                     |  WaitingInstanceRelease  |
      |  AccessLinkClientDisconnectTimeout |  WaitingInstanceRelease  |
      |  AccessLinkServerDisconnect        |  WaitingInstanceRelease  |
      |  InstanceNoInputTimeout            |    InstanceApplying      |
      |  InstanceError                     |    InstanceApplying      |
      |  InstanceReleaseSuccess            |    InstanceApplying      |
      |  InstanceReleaseFailed             |    InstanceApplying      |
      |  InstanceReleaseRetry              |    InstanceApplying      |
      |  InstanceReleaseRetryOut           |    InstanceApplying      |
      |  CloudUserEnqueueConfirmYes        |    InstanceApplying      |
      |  CloudUserDequeue                  |    InstanceApplying      |
      |  CloudUserEnqueue                  |    InstanceApplying      |
      |     DoRefreshStoken                |    InstanceApplying      |
      |    DoRefreshStokenSuccess          |    InstanceApplying      |
      |    DoRefreshStokenFailed           |    InstanceApplying      |
      |      DoChangeResolution            |    InstanceApplying      |
      |  DoChangeResolutionSuccess         |    InstanceApplying      |
      |   DoChangeResolutionFailed         |    InstanceApplying      |

  Scenario: from InstanceApplying to Enqueue
    Given 用户创建一个 "InstanceApplying" 的状态机
    When 用户触发"SyncApplyInstanceNoIdle"事件
    Then 这个状态机的状态应该是"WaitingConfirmEnqueue"
    When 用户触发"CloudUserEnqueue"事件
    Then 这个状态机的状态应该是"Enqueue"
    When 设置paas的最大实例数为"0"
    And 用户触发"CloudUserDequeue"事件
    Then 这个状态机的状态应该是"Enqueue"


  Scenario Outline: test the InstanceApplying status with paas service
    Given 用户创建一个 "InstanceApplying" 的状态机
    And 设置paas的错误响应次数为"<num>"
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |  num  |           event                 |   status  |
      |    0  |  SyncApplyInstanceSuccess       | InService |
      |    1  |  SyncApplyInstanceRpcException  | InService |
      |    2  |  SyncApplyInstanceRpcException  | InService |
      |    3  |  SyncApplyInstanceRpcException  | Finished  |
      |    4  |  SyncApplyInstanceRpcException  | Finished  |



  Scenario Outline: test the WaitingInstanceRelease status
    Given 用户创建一个 "WaitingInstanceRelease" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |  WaitingInstanceRelease  |
      |  AccessLinkFailed                  |  WaitingInstanceRelease  |
      |  SyncApplyInstanceSuccess          |  WaitingInstanceRelease  |
      |  SyncApplyInstanceNoIdle           |  WaitingInstanceRelease  |
      |  SyncApplyInstanceRpcException     |  WaitingInstanceRelease  |
      |  SyncApplyInstanceRetry            |  WaitingInstanceRelease  |
      |  SyncApplyInstanceRetryOut         |  WaitingInstanceRelease  |
      |  SyncApplyInstanceError            |  WaitingInstanceRelease  |
      |  AsyncInstancePreparationSuccess   |         Finished         |
      |  AsyncInstancePreparationFailed    |         Finished         |
      |  CloudServiceApply                 |  WaitingInstanceRelease  |
      |  CloudServiceTimeout               |  WaitingInstanceRelease  |
      |  CloudUserExit                     |  WaitingInstanceRelease  |
      |  AccessLinkClientDisconnectTimeout |  WaitingInstanceRelease  |
      |  AccessLinkServerDisconnect        |  WaitingInstanceRelease  |
      |  InstanceNoInputTimeout            |  WaitingInstanceRelease  |
      |  InstanceError                     |  WaitingInstanceRelease  |
      |  InstanceReleaseSuccess            |  WaitingInstanceRelease  |
      |  InstanceReleaseFailed             |  WaitingInstanceRelease  |
      |  InstanceReleaseRetry              |  WaitingInstanceRelease  |
      |  InstanceReleaseRetryOut           |  WaitingInstanceRelease  |
      |  CloudUserEnqueueConfirmYes        |  WaitingInstanceRelease  |
      |  CloudUserDequeue                  |  WaitingInstanceRelease  |
      |  CloudUserEnqueue                  |  WaitingInstanceRelease  |
      |     DoRefreshStoken                |  WaitingInstanceRelease  |
      |    DoRefreshStokenSuccess          |  WaitingInstanceRelease  |
      |    DoRefreshStokenFailed           |  WaitingInstanceRelease  |
      |      DoChangeResolution            |  WaitingInstanceRelease  |
      |  DoChangeResolutionSuccess         |  WaitingInstanceRelease  |
      |   DoChangeResolutionFailed         |  WaitingInstanceRelease  |

  Scenario Outline: test the WaitingInstanceRelease status with paas service
    Given 用户创建一个 "WaitingInstanceRelease" 的状态机
    When 设置paas的错误响应次数为"<num>"
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |  num  |           event                   |   status  |
      |    0  |  AsyncInstancePreparationSuccess  | Finished  |
      |    1  |  AsyncInstancePreparationSuccess  | Finished  |
      |    2  |  AsyncInstancePreparationSuccess  | Finished  |
      |    3  |  AsyncInstancePreparationSuccess  | InService |
      |    4  |  AsyncInstancePreparationSuccess  | InService |
      |    0  |  AsyncInstancePreparationFailed   | Finished  |
      |    1  |  AsyncInstancePreparationFailed   | Finished  |
      |    2  |  AsyncInstancePreparationFailed   | Finished  |
      |    3  |  AsyncInstancePreparationFailed   | InService |
      |    4  |  AsyncInstancePreparationFailed   | InService |


  Scenario Outline: test the InstanceReleaseing status
    Given 用户创建一个 "InstanceReleaseing" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |       status         |
      |  AccessLinkSuccess                 |  InstanceReleaseing  |
      |  AccessLinkFailed                  |  InstanceReleaseing  |
      |  SyncApplyInstanceSuccess          |  InstanceReleaseing  |
      |  SyncApplyInstanceNoIdle           |  InstanceReleaseing  |
      |  SyncApplyInstanceRpcException     |  InstanceReleaseing  |
      |  SyncApplyInstanceRetry            |  InstanceReleaseing  |
      |  SyncApplyInstanceRetryOut         |  InstanceReleaseing  |
      |  SyncApplyInstanceError            |  InstanceReleaseing  |
      |  AsyncInstancePreparationSuccess   |  InstanceReleaseing  |
      |  AsyncInstancePreparationFailed    |  InstanceReleaseing  |
      |  CloudServiceApply                 |  InstanceReleaseing  |
      |  CloudServiceTimeout               |  InstanceReleaseing  |
      |  CloudUserExit                     |  InstanceReleaseing  |
      |  AccessLinkClientDisconnectTimeout |  InstanceReleaseing  |
      |  AccessLinkServerDisconnect        |  InstanceReleaseing  |
      |  InstanceNoInputTimeout            |  InstanceReleaseing  |
      |  InstanceError                     |  InstanceReleaseing  |
      |  InstanceReleaseSuccess            |      Finished        |
      |  InstanceReleaseFailed             |      Finished        |
      |  InstanceReleaseRetry              |      Finished        |
      |  InstanceReleaseRetryOut           |      InService       |
      |  CloudUserEnqueueConfirmYes        |  InstanceReleaseing  |
      |  CloudUserDequeue                  |  InstanceReleaseing  |
      |  CloudUserEnqueue                  |  InstanceReleaseing  |
      |     DoRefreshStoken                |  InstanceReleaseing  |
      |    DoRefreshStokenSuccess          |  InstanceReleaseing  |
      |    DoRefreshStokenFailed           |  InstanceReleaseing  |
      |      DoChangeResolution            |  InstanceReleaseing  |
      |  DoChangeResolutionSuccess         |  InstanceReleaseing  |
      |   DoChangeResolutionFailed         |  InstanceReleaseing  |


  Scenario Outline: test the InService status
    Given 用户创建一个 "InService" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |        status       |
      |  AccessLinkSuccess                 |      InService      |
      |  AccessLinkFailed                  |      InService      |
      |  SyncApplyInstanceSuccess          |      InService      |
      |  SyncApplyInstanceNoIdle           |      InService      |
      |  SyncApplyInstanceRpcException     |      InService      |
      |  SyncApplyInstanceRetry            |      InService      |
      |  SyncApplyInstanceRetryOut         |      InService      |
      |  SyncApplyInstanceError            |      InService      |
      |  AsyncInstancePreparationSuccess   |      InService      |
      |  AsyncInstancePreparationFailed    |      InService      |
      |  CloudServiceApply                 |      InService      |
      |  CloudServiceTimeout               |      Finished       |
      |  CloudUserExit                     |      Finished       |
      |  AccessLinkClientDisconnectTimeout |      Finished       |
      |  AccessLinkServerDisconnect        |      Finished       |
      |  InstanceNoInputTimeout            |      Finished       |
      |  InstanceError                     |      Finished       |
      |  InstanceReleaseSuccess            |      Finished       |
      |  InstanceReleaseFailed             |      InService      |
      |  InstanceReleaseRetry              |      InService      |
      |  InstanceReleaseRetryOut           |      InService      |
      |  CloudUserEnqueueConfirmYes        |      InService      |
      |  CloudUserDequeue                  |      InService      |
      |  CloudUserEnqueue                  |      InService      |
      |     DoRefreshStoken                |      InService      |
      |    DoRefreshStokenSuccess          |      InService      |
      |    DoRefreshStokenFailed           |      Finished       |
      |      DoChangeResolution            |      InService      |
      |  DoChangeResolutionSuccess         |      InService      |
      |   DoChangeResolutionFailed         |      Finished       |



  Scenario Outline: test the WaitingConfirmEnqueue status
    Given 用户创建一个 "WaitingConfirmEnqueue" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |  WaitingConfirmEnqueue   |
      |  AccessLinkFailed                  |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceSuccess          |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceNoIdle           |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceRpcException     |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceRetry            |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceRetryOut         |  WaitingConfirmEnqueue   |
      |  SyncApplyInstanceError            |  WaitingConfirmEnqueue   |
      |  AsyncInstancePreparationSuccess   |  WaitingConfirmEnqueue   |
      |  AsyncInstancePreparationFailed    |  WaitingConfirmEnqueue   |
      |  CloudServiceApply                 |  WaitingConfirmEnqueue   |
      |  CloudServiceTimeout               |  WaitingConfirmEnqueue   |
      |  CloudUserExit                     |        Finished          |
      |  AccessLinkClientDisconnectTimeout |        Finished          |
      |  AccessLinkServerDisconnect        |        Finished          |
      |  InstanceNoInputTimeout            |  WaitingConfirmEnqueue   |
      |  InstanceError                     |  WaitingConfirmEnqueue   |
      |  InstanceReleaseSuccess            |  WaitingConfirmEnqueue   |
      |  InstanceReleaseFailed             |  WaitingConfirmEnqueue   |
      |  InstanceReleaseRetry              |  WaitingConfirmEnqueue   |
      |  InstanceReleaseRetryOut           |  WaitingConfirmEnqueue   |
      |  CloudUserEnqueueConfirmYes        |  WaitingConfirmEnqueue   |
      |  CloudUserDequeue                  |         InService        |
      |  CloudUserEnqueue                  |         Enqueue          |
      |     DoRefreshStoken                |  WaitingConfirmEnqueue   |
      |    DoRefreshStokenSuccess          |  WaitingConfirmEnqueue   |
      |    DoRefreshStokenFailed           |  WaitingConfirmEnqueue   |
      |      DoChangeResolution            |  WaitingConfirmEnqueue   |
      |  DoChangeResolutionSuccess         |  WaitingConfirmEnqueue   |
      |   DoChangeResolutionFailed         |  WaitingConfirmEnqueue   |



  Scenario Outline: test the Enqueue status
    Given 用户创建一个 "Enqueue" 的状态机
    When 用户触发"<event>"事件
    Then 这个状态机的状态应该是"<status>"
    Examples:
      |              event                 |         status       |
      |  AccessLinkSuccess                 |        Enqueue       |
      |  AccessLinkFailed                  |        Enqueue       |
      |  SyncApplyInstanceSuccess          |        Enqueue       |
      |  SyncApplyInstanceNoIdle           |        Enqueue       |
      |  SyncApplyInstanceRpcException     |        Enqueue       |
      |  SyncApplyInstanceRetry            |        Enqueue       |
      |  SyncApplyInstanceRetryOut         |        Enqueue       |
      |  SyncApplyInstanceError            |        Enqueue       |
      |  AsyncInstancePreparationSuccess   |        Enqueue       |
      |  AsyncInstancePreparationFailed    |        Enqueue       |
      |  CloudServiceApply                 |        Enqueue       |
      |  CloudServiceTimeout               |        Enqueue       |
      |  CloudUserExit                     |        Finished      |
      |  AccessLinkClientDisconnectTimeout |        Finished      |
      |  AccessLinkServerDisconnect        |        Finished      |
      |  InstanceNoInputTimeout            |        Enqueue       |
      |  InstanceError                     |        Enqueue       |
      |  InstanceReleaseSuccess            |        Enqueue       |
      |  InstanceReleaseFailed             |        Enqueue       |
      |  InstanceReleaseRetry              |        Enqueue       |
      |  InstanceReleaseRetryOut           |        Enqueue       |
      |  CloudUserEnqueueConfirmYes        |        Enqueue       |
      |  CloudUserDequeue                  |       Inservice      |
      |  CloudUserEnqueue                  |       Enqueue        |
      |     DoRefreshStoken                |        Enqueue       |
      |    DoRefreshStokenSuccess          |        Enqueue       |
      |    DoRefreshStokenFailed           |        Enqueue       |
      |      DoChangeResolution            |        Enqueue       |
      |  DoChangeResolutionSuccess         |        Enqueue       |
      |   DoChangeResolutionFailed         |        Enqueue       |
