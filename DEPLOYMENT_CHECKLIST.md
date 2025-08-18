# Railway Deployment Troubleshooting

## Quick Health Checks
```bash
# Check if migrations applied
railway run python manage.py showmigrations

# Test database connection
railway run python manage.py dbshell

# Verify static files
railway run python manage.py collectstatic --dry-run

# Check environment variables
railway run python manage.py shell -c "import os; print('DEBUG:', os.getenv('DEBUG')); print('DB:', os.getenv('PGDATABASE'))"
```

## Common Issues & Solutions

### Migration Hanging
- Restart PostgreSQL service in Railway dashboard
- Check for locked tables: `SELECT * FROM pg_locks;`

### Build Failures
- Verify Python version in runtime.txt
- Check dependency conflicts in build logs
- Ensure psycopg2-binary (not psycopg2) in requirements

### App Failed to Respond
- Verify Procfile uses `$PORT` variable (our Procfile is correct)
- Check ALLOWED_HOSTS includes Railway domains
- Monitor gunicorn startup in logs

### Database Connection Issues
- Verify all PGDATABASE, PGUSER, PGPASSWORD, PGHOST set
- Test connection timeout settings
- Check if build phase properly skips database