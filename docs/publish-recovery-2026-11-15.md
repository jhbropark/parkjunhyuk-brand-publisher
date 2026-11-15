# Daily publishing recovery evidence

Status: NOT resumed. Pending marker deliberately retained until credentials
are repaired and the reconciliation/resumption decision is approved.

## October 25 partial success

Marker run: 40155947103.
Job logs: https://github.com/jhbropark/parkjunhyuk-brand-publisher/actions/runs/40155947103

The publish job returned two Instagram success IDs and a Facebook post ID;
the committed plan contains matching permalinks. LinkedIn failed at userinfo
(HTTP 401), before a LinkedIn post could be created by that attempt.

| Item | Result | Evidence |
| --- | --- | --- |
| Instagram carousel | published | 17973263970174817; https://www.instagram.com/p/De5ru4FACZc/ |
| Instagram reel | published | 17914839078470243; https://www.instagram.com/reel/De5ry1ZgLLu/ |
| Facebook | published | post_id 1140846082456388_122123516067366256; https://www.facebook.com/1140846082456388_122123516067366256 |
| LinkedIn | failed before publication | HTTP 401 at /v2/userinfo |

This is a historical API/log-and-state reconciliation, not a claim that every
post is currently publicly visible. No posts were changed or created.

## Before resumption

1. Repair this repository's LinkedIn credentials, then run the identity
   preflight in a secure environment. It prints no token or provider body.
2. Preserve this old plan and its links as an archive. Do not republish the old
   October 25 content merely to clear the marker.
3. Reconcile the marker with this evidence and document the decision for the
   failed LinkedIn item before removing the pending marker.
4. Enable a fresh scheduled run only after authorization. A preflight is not
   proof of all media-upload/post scopes; retain the fail-closed gate.
5. Verify the subsequent run's provider outcomes and saved links.

The new preflight runs after the unresolved marker guard but before generation
and before any Instagram/Facebook post. This prevents the observed expired
LinkedIn identity failure from consuming content-generation resources or causing
a fresh partial-publication batch. The existing unresolved guard is unchanged.
