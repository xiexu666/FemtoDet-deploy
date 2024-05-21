_base_ = './yolox_s_8x8_300e_coco.py'
classes = ('open', 'short', 'mousebite', 'spur', 'copper', 'pin-hole')
load_from = 'yolox_tiny_8x8_300e_coco_20211124_171234-b4047906.pth'
work_dir = 'work_dirs_pcb/yolox_tiny_8x8_300e_coco_pcb_mosaic'

# model settings
model = dict(
    random_size_range=(10, 20),
    backbone=dict(deepen_factor=0.33, widen_factor=0.375),
    neck=dict(in_channels=[96, 192, 384], out_channels=96),
    bbox_head=dict(num_classes=len(classes), in_channels=96, feat_channels=96))

img_scale = (640, 640)  # height, width
data_root = '/home/xiexu/code/pcb/DeepPCB-to-COCO-main/JSONdump//'

train_pipeline = [
    # dict(type='Mosaic', img_scale=img_scale, pad_val=114.0),
    # dict(
    #     type='RandomAffine',
    #     scaling_ratio_range=(0.5, 1.5),
    #     border=(-img_scale[0] // 2, -img_scale[1] // 2)),
    dict(type='YOLOXHSVRandomAug'),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Resize', img_scale=img_scale, keep_ratio=True),
    dict(
        type='Pad',
        pad_to_square=True,
        pad_val=dict(img=(114.0, 114.0, 114.0))),
    dict(type='FilterAnnotations', min_gt_bbox_wh=(1, 1), keep_empty=False),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(416, 416),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Pad',
                pad_to_square=True,
                pad_val=dict(img=(114.0, 114.0, 114.0))),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img'])
        ])
]
dataset_type = 'CocoDataset'

train_dataset = dict(
    type='MultiImageMixDataset',
    dataset=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'instances_train2014.json',
        img_prefix=data_root + 'images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations', with_bbox=True)
        ],
        filter_empty_gt=False,
    ),
    pipeline=train_pipeline)



# data = dict(
#     train=train_dataset,
#     val=dict(pipeline=test_pipeline),
#     test=dict(pipeline=test_pipeline))

data = dict(
    samples_per_gpu=8,
    workers_per_gpu=4,
    persistent_workers=True,
    train=train_dataset,
    val=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'instances_test2014.json',
        img_prefix=data_root + 'images/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'instances_test2014.json',
        img_prefix=data_root + 'images/',
        pipeline=test_pipeline))