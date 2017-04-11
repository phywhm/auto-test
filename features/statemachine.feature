# Created by xiama at 4/6/17
Feature: state machine testing
  # Enter feature description here

  Scenario Outline: test the Created status
    Given user create a machine with "Created" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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


  Scenario Outline: test the Linked status
    Given user create a machine with "Linked" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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


  Scenario Outline: test the Linked status with queue status
    Given user create a machine with "Linked" status
    When I set the status of product to "<islimit>"
    And the paas do not return the address message
    When I set the size of queue to "<queue_size>"
    When user fire the "CloudServiceApply" event
    Then the status of the machine should be "<status>"
    Examples:
      |  islimit  |  queue_size  |         status        |
      |    over   |      2       | WaitingConfirmEnqueue |
      |  notover  |      3       | WaitingConfirmEnqueue |
      |    over   |      0       | WaitingConfirmEnqueue |
      |  notover  |      0       |    InstanceApplying   |


  Scenario Outline: test the InstanceApplying status
    Given user create a machine with "InstanceApplying" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
    Examples:
      |              event                 |          status          |
      |  AccessLinkSuccess                 |   InstanceApplying       |
      |  AccessLinkFailed                  |   InstanceApplying       |
      |  SyncApplyInstanceSuccess          |         InService           |
      |  SyncApplyInstanceNoIdle           |         WaitingConfirmEnqueue  or Enqueue     |
      |  SyncApplyInstanceRpcException     |         InService           |
      |  SyncApplyInstanceRetry            |         InService           |
      |  SyncApplyInstanceRetryOut         |         Finished           |
      |  SyncApplyInstanceError            |         Finished           |
      |  AsyncInstancePreparationSuccess   |         InService           |
      |  AsyncInstancePreparationFailed    |         InstanceReleaseing           |
      |  CloudServiceApply                 |         InstanceApplying           |
      |  CloudServiceTimeout               |         InstanceApplying           |
      |  CloudUserExit                     |        WaitingInstanceRelease          |
      |  AccessLinkClientDisconnectTimeout |        WaitingInstanceRelease          |
      |  AccessLinkServerDisconnect        |        WaitingInstanceRelease          |
      |  InstanceNoInputTimeout            |         InstanceApplying           |
      |  InstanceError                     |         InstanceApplying           |
      |  InstanceReleaseSuccess            |         InstanceApplying           |
      |  InstanceReleaseFailed             |         InstanceApplying           |
      |  InstanceReleaseRetry              |         InstanceApplying           |
      |  InstanceReleaseRetryOut           |         InstanceApplying           |
      |  CloudUserEnqueueConfirmYes        |         InstanceApplying           |
      |  CloudUserDequeue                  |         InstanceApplying           |
      |  CloudUserEnqueue                  |         InstanceApplying           |


  Scenario Outline: test the InstanceApplying status with paas service
    Given user create a machine with "InstanceApplying" status
    When I set the paas failure times to "<num>"
    And the paas do not return the address message
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
    Examples:
      |  num  |           event                 |   status  |
      |    0  |  SyncApplyInstanceSuccess       | InstanceApplying |
      |    1  |  SyncApplyInstanceRpcException  | InstanceApplying |
      |    2  |  SyncApplyInstanceRpcException  | InstanceApplying |
      |    3  |  SyncApplyInstanceRpcException  | Finished |
      |    4  |  SyncApplyInstanceRpcException  | Finished  |



  Scenario Outline: test the WaitingInstanceRelease status
    Given user create a machine with "WaitingConfirmEnqueue" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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

  Scenario Outline: test the WaitingInstanceRelease status with paas service
    Given user create a machine with "WaitingConfirmEnqueue" status
    When I set the paas failure times to "<num>"
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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
    Given user create a machine with "InstanceReleaseing" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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


  Scenario Outline: test the InService status
    Given user create a machine with "InstanceReleaseing" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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



  Scenario Outline: test the WaitingConfirmEnqueue status
    Given user create a machine with "WaitingConfirmEnqueue" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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
      |  CloudUserDequeue                  |  WaitingConfirmEnqueue   |
      |  CloudUserEnqueue                  |         Enqueue          |



  Scenario Outline: test the Enqueue status
    Given user create a machine with "Enqueue" status
    When user fire the "<event>" event
    Then the status of the machine should be "<status>"
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
      |  CloudUserDequeue                  |        Enqueue       |
      |  CloudUserEnqueue                  |       Inservice      |
