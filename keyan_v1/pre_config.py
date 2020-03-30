import pandas as pd

# app: raw, one_hot, sub, mean, order, norm, nlp
all_cfg = {
    'before': {
        'admiss_times': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'cp_status': {
            'app': 'one_hot',
            'fill_nan': 11,
        },
        'charge_type': {
            'app': 'one_hot',
            'fill_nan': 2,
        },
        'visit_type': {
            'app': 'one_hot',
            'fill_nan': 1,
        },
        'admiss_status': {
            'app': 'raw',
            'fill_nan': 3,
        },
        'admiss_diag': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'birth_weight': {
            'app': 'norm',
            'fill_nan': 'mean',
        },
        'admiss_weight': {
            'app': 'norm',
            'fill_nan': 'mean',
        },
        'admiss_path': {
            'app': 'one_hot',
            'fill_nan': 2,
        },
        'tssf': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
    },
    'middle': {
        'wsw_norm': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'clinic_diag': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'responce_type': {
            'app': 'one_hot',
            'fill_nan': '02',
        },
        'times_billed': {
            'app': 'raw',
            'fill_nan': 1,
        },
        'balance': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'total_charge': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge1': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge2': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge3': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge4': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge5': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge6': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge7': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge8': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge9': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge10': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge11': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge12': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge13': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'charge14': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'sex': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'blood_type': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'diagnosis_date': {
            'app': 'sub',
            'fill_nan': 0,
        },
        'allergy_medicine': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'rescue_times': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'success_times': {
            'app': 'raw',
            'fill_nan': 0,
        },
        'followup_mark': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'quality_level': {
            'app': 'order',
            'fill_nan': 0,
        },
        'pay_flag': {
            'app': 'one_hot',
            'fill_nan': 3,
        },
        'local_flag': {
            'app': 'one_hot',
            'fill_nan': 1,
        },
        'ycy_flay': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'birth_date': {
            'app': 'sub',
            'fill_nan': 0,
        },
        'marry_code': {
            'app': 'one_hot',
            'fill_nan': 2,
        },
        'nation_code': {
            'app': 'one_hot',
            'fill_nan': 1,
        },
        'occupation_code': {
            'app': 'one_hot',
            'fill_nan': 7,
        },
        'vip_code': {
            'app': 'one_hot',
            'fill_nan': 9,
        },

    },
    'after': {
        'dis_diag_no': {
            'app': 'order',
            'fill_nan': 1,
        },
        'dis_diag_type': {
            'app': 'one_hot',
            'fill_nan': 2,
        },
        'dis_diag_status': {
            'app': 'order',
            'fill_nan': 2,
        },
        'dis_diag': {
            'app': 'one_hot',
            'fill_nan': 0,
        },
        'dis_diag_comment': {
            'app': 'nlp',
            'fill_nan': 0,
        },
        'dis_status': {
            'app': 'one_hot',
            'fill_nan': 1,
        },
    }
}
