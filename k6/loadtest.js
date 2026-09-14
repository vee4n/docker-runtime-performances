import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '60s',
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:3000';

export default function () {
  const res = http.get(BASE_URL + '/compute');
  check(res, {
    'status 200': (r) => r.status === 200,
  });
}
