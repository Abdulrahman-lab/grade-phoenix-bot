# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0-dev] - 2025-07-04

### Added
- Telegram University Bot with secure, user-friendly grade notifications
- No password storage: passwords are used only for login and immediately discarded
- Token-based session management for user security
- Dual-language (Arabic/English) motivational quotes with intelligent translation (10 retry attempts)
- User-facing security and privacy messaging throughout the bot
- Admin dashboard and broadcast system with comprehensive analytics
- Real-time security event logging and statistics
- Comprehensive security headers (CSP, HSTS, X-Frame-Options)
- Automated database migration for no-password-storage policy
- Enhanced logging system with colored output and file rotation
- Railway deployment support with automatic webhook configuration
- Relogin button for easy session renewal
- Manual keyboard refresh functionality
- Translation retry logic with immediate attempts (no delays)

### Improved
- Clear, simple user interface with main and admin keyboards
- Transparent credential handling and privacy policy
- Automated daily quote broadcast to all users
- Webhook URL construction with multiple Railway environment variable support
- Keyboard updates immediately after user login
- Quote formatting with proper spacing and disclaimers
- Translation reliability with comprehensive validation
- Database migration logging and error handling
- Production deployment stability and monitoring

### Changed
- All GitHub repository links now include '?refresh' to ensure preview is always up to date.

## [v1.0.0] - 2025-07-04
### Major Release
- **Syrian State Visual Identity:** The project now uses the Syrian State Visual Identity for its branding and UI.
- **Sticky User Flow Fixes:** Users can always cancel, recover from errors, and never get stuck in any flow.
- **Context-Aware Motivational Quotes:** Quotes are now relevant to the user's grade situation, not random.
- **Transparency Improvements:** All messages and README clarify that passwords are never stored, and the GitHub repo is public for full transparency ([GitHub](https://github.com/sispt/grade-phoenix-bot?refresh)).
- **Settings Menu Overhaul:** Settings are now functional, with a GitHub button and improved navigation.
- **Logout Button Restored:** The logout button is back in the main keyboard for easy access.
- **Robust Error/Cancel Handling:** Cancel and error recovery are available everywhere, always returning the user to a safe state.
- **General Stability:** All main flows tested and refined for reliability and user experience.
- All GitHub repository links now include '?refresh' to ensure preview is always up to date.

## [2.0.0] - 2025-07-05
### Major Release
- New GraphQL API system with robust error handling
- Full PostgreSQL storage and migration from old system
- Enhanced admin dashboard and broadcast tools
- Improved grade notification and quote system
- Security and privacy improvements
- Compatibility and bug fixes

---

_This changelog summarizes major features and improvements for each release. For detailed commit history, see the repository's commit log._