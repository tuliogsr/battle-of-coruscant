import sys
from time import sleep
import pygame
from Construindo.bullet import Bullet
from Construindo.alien import Alien
import json

class GameFunctions:
    @staticmethod
    def check_keydown_events(event, ai_settings, screen, ship, bullets):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            GameFunctions.fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()

    @staticmethod
    def check_keyup_events(event, ship):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False

    @staticmethod
    def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                GameFunctions.check_keydown_events(event, ai_settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                GameFunctions.check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                GameFunctions.check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

    @staticmethod
    def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Contagem regressiva de 5 a 0
            for i in range(5, 0, -1):
                screen.fill(ai_settings.bg_color)
                font = pygame.font.SysFont(None, 74)
                countdown_text = font.render(str(i), True, (255, 0, 0))
                countdown_rect = countdown_text.get_rect(center=screen.get_rect().center)
                screen.blit(countdown_text, countdown_rect)
                pygame.display.flip()
                sleep(1)

            # Reset the game settings.
            ai_settings.initialize_dynamic_settings()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center the ship.
            GameFunctions.create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

    @staticmethod
    def fire_bullet(ai_settings, screen, ship, bullets):
        """Fire a bullet, if limit not reached yet."""
        # Create a new bullet, add to bullets group.
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

    @staticmethod
    def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen, each pass through the loop.
        screen.fill(ai_settings.bg_color)

        # Redraw all bullets, behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)

        # Draw the score information.
        sb.show_score()

        # Draw the play button if the game is inactive.
        if not stats.game_active:
            play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    @staticmethod
    def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """Update position of bullets, and get rid of old bullets."""
        # Update bullet positions.
        bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        GameFunctions.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

    @staticmethod
    def check_high_score(stats, sb):
        """Check to see if there's a new high score."""
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()
            stats.save_high_score()
            GameFunctions.save_high_score(stats.high_score)

    @staticmethod
    def save_high_score(high_score):
        """Save the high score to a file."""
        file_name = "Dados/high_score.json"
        with open(file_name, "w") as file:
            json.dump(high_score, file)

    @staticmethod
    def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                stats.score += ai_settings.alien_points * len(aliens)
                sb.prep_score()
            GameFunctions.check_high_score(stats, sb)

        if len(aliens) == 0:
            # If the entire fleet is destroyed, start a new level.
            bullets.empty()
            ai_settings.increase_speed()

            # Increase level.
            stats.level += 1
            sb.prep_level()

            GameFunctions.create_fleet(ai_settings, screen, ship, aliens)

    @staticmethod
    def check_fleet_edges(ai_settings, aliens):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in aliens.sprites():
            if alien.check_edges():
                GameFunctions.change_fleet_direction(ai_settings, aliens)
                break

    @staticmethod
    def change_fleet_direction(ai_settings, aliens):
        """Drop the entire fleet, and change the fleet's direction."""
        for alien in aliens.sprites():
            alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1

    @staticmethod
    def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """Respond to ship being hit by alien."""
        if stats.ships_left > 0:
            # Decrement ships_left.
            stats.ships_left -= 1

            # Update scoreboard.
            sb.prep_ships()

        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet, and center the ship.
        GameFunctions.create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)

    @staticmethod
    def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                GameFunctions.ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
                break

    @staticmethod
    def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """
        Check if the fleet is at an edge,
        then update the postions of all aliens in the fleet.
        """
        GameFunctions.check_fleet_edges(ai_settings, aliens)
        aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(ship, aliens):
            GameFunctions.ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # Look for aliens hitting the bottom of the screen.
        GameFunctions.check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

    @staticmethod
    def get_number_aliens_x(ai_settings, alien_width):
        """Determine the number of aliens that fit in a row."""
        available_space_x = ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    @staticmethod
    def get_number_rows(ai_settings, ship_height, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        available_space_y = (ai_settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    @staticmethod
    def create_alien(ai_settings, screen, aliens, alien_number, row_number):
        """Create an alien, and place it in the row."""
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)

    @staticmethod
    def create_fleet(ai_settings, screen, ship, aliens):
        """Create a full fleet of aliens."""
        # Create an alien, and find number of aliens in a row.
        alien = Alien(ai_settings, screen)
        number_aliens_x = GameFunctions.get_number_aliens_x(ai_settings, alien.rect.width)
        number_rows = GameFunctions.get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

        # Create the fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                GameFunctions.create_alien(ai_settings, screen, aliens, alien_number, row_number)

    @staticmethod
    def save_score(nickname, score):
        """Save the player's score."""
        file_name = "Dados/player_scores.json"
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[nickname] = max(score, data.get(nickname, 0))

        # Manter apenas os 5 melhores scores
        top_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)[:5]
        data = {k: v for k, v in top_scores}

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)