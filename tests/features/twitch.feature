Feature: Twitch Mobile Search
  As a mobile user of Twitch
  I want to search for game streams
  So that I can watch my favorite games

  Background:
    Given I am on the Twitch mobile site

  Scenario: Search for StarCraft II streams
    When I click on the search button
    And I search for "StarCraft II"
    And I scroll down 2 times
    Then I should see search results
    When I click on a streamer
    Then the video should play
    And I take a screenshot

  Scenario: Handle mature content warning
    When I click on the search button
    And I search for "StarCraft II"
    And I click on a streamer
    Then I should handle mature content warning if present
    And the video should play
    And I take a screenshot

  Scenario Outline: Search for different games
    When I click on the search button
    And I search for "<game>"
    Then I should <result>

    Examples:
      | game                      | result               |
      | League of Legends         | see search results   |
      | Fortnite                  | see search results   |
      | Dota 2                    | see search results   |
      | RandomInvalidGameName12345| see no results       | 