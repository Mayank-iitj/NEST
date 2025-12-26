# Production Deployment Checklist

## Pre-Deployment Security

- [ ] Generated secure SECRET_KEY (min 32 characters)
- [ ] Generated secure ENCRYPTION_KEY (32 bytes)
- [ ] Changed default database passwords
- [ ] Changed default Redis password
- [ ] Reviewed all environment variables
- [ ] Removed any test/debug credentials
- [ ] Enabled HTTPS/TLS
- [ ] Configured CORS for production domains only

## API Keys & Credentials

- [ ] Added valid OPENAI_API_KEY (or confirmed mock mode acceptable)
- [ ] Added WHATSAPP_API_KEY or confirmed mock mode
- [ ] Added TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
- [ ] Configured SMTP credentials if using email
- [ ] Stored all secrets securely (not in git)

## Database

- [ ] PostgreSQL instance created
- [ ] Database initialized with init.sql
- [ ] Database backups configured
- [ ] Connection pooling configured
- [ ] Indexes verified

## Infrastructure

- [ ] Docker images built successfully
- [ ] Health checks passing
- [ ] Redis cache accessible
- [ ] Nginx reverse proxy configured
- [ ] Rate limiting tested
- [ ] Log aggregation setup

## Application Configuration

- [ ] ENVIRONMENT set to "production"
- [ ] CORS_ORIGINS updated for production domains
- [ ] API URL updated in frontend
- [ ] Workers configured appropriately (4 for backend)
- [ ] File upload limits set
- [ ] Session timeout configured

## Security Hardening

- [ ] Non-root user in Docker containers
- [ ] Security headers configured in nginx
- [ ] SQL injection protection verified
- [ ] XSS protection headers enabled
- [ ] CSRF tokens implemented where needed
- [ ] Rate limiting active on OTP endpoints
- [ ] Password hashing with bcrypt confirmed

## Monitoring & Logging

- [ ] Application logs accessible
- [ ] Error tracking setup (Sentry recommended)
- [ ] Uptime monitoring configured
- [ ] Database monitoring enabled
- [ ] Alert notifications configured
- [ ] Log retention policy set

## Testing

- [ ] Smoke tests passed
- [ ] OTP flow tested end-to-end
- [ ] AI features tested (missing fields, risk scoring)
- [ ] Multi-channel messaging tested
- [ ] Dashboard metrics verified
- [ ] Mobile responsiveness checked
- [ ] Cross-browser testing done

## Performance

- [ ] Backend response times < 200ms (p95)
- [ ] Frontend load time < 2s
- [ ] Database queries optimized
- [ ] Static assets cached properly
- [ ] Gzip compression enabled
- [ ] CDN configured (if needed)

## Compliance & Legal

- [ ] HIPAA compliance reviewed (if handling real PHI)
- [ ] GDPR compliance verified (if serving EU)
- [ ] Terms of service updated
- [ ] Privacy policy in place
- [ ] Data retention policy documented
- [ ] Consent forms implemented

## Documentation

- [ ] README.md updated with production URLs
- [ ] API documentation accessible
- [ ] Deployment guide reviewed
- [ ] Runbook for common issues created
- [ ] Architecture diagram updated
- [ ] Contact information for support added

## Backup & Recovery

- [ ] Database backup schedule configured
- [ ] Backup restoration tested
- [ ] Disaster recovery plan documented
- [ ] Data retention policy implemented
- [ ] Rollback procedure tested

## Go-Live

- [ ] Staging environment tested
- [ ] Production deployment rehearsed
- [ ] DNS records configured
- [ ] SSL certificates installed
- [ ] All services started
- [ ] Health checks green
- [ ] First real user flow tested
- [ ] Team notified of go-live

## Post-Deployment

- [ ] Monitor logs for errors (first 24 hours)
- [ ] Check performance metrics
- [ ] Verify all integrations working
- [ ] Test from different locations/networks
- [ ] Gather initial user feedback
- [ ] Document any issues encountered
- [ ] Schedule post-launch review

## Platform-Specific (Choose One)

### Railway
- [ ] Services linked to GitHub repo
- [ ] Environment variables configured
- [ ] PostgreSQL plugin added
- [ ] Redis plugin added
- [ ] Auto-deploy enabled
- [ ] Custom domain configured (optional)

### Render
- [ ] PostgreSQL database created
- [ ] Redis instance created
- [ ] Backend web service deployed
- [ ] Frontend static site deployed
- [ ] Environment variables set
- [ ] Auto-deploy from GitHub enabled

### AWS
- [ ] ECS cluster created
- [ ] RDS PostgreSQL instance running
- [ ] ElastiCache Redis configured
- [ ] Load balancer setup
- [ ] Auto-scaling configured
- [ ] CloudWatch monitoring enabled

### Docker Compose (Self-Hosted)
- [ ] Server provisioned
- [ ] Docker and Docker Compose installed
- [ ] SSL certificates obtained
- [ ] Firewall rules configured
- [ ] Automated backups setup
- [ ] Monitoring tools installed

## Critical Warnings

⚠️ **Never commit these to git:**
- .env files
- SSL private keys
- API credentials
- Encryption keys
- Database passwords

⚠️ **Before accepting real patient data:**
- Complete security audit
- Obtain regulatory approval
- Implement audit trails
- Setup compliance monitoring
- Legal review required

⚠️ **Performance baselines:**
- Response time: < 200ms (p95)
- Uptime: > 99.5%
- Error rate: < 0.1%
- OTP delivery: < 5 seconds
