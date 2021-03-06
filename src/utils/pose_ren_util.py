import numpy as np

def combine_gt_init_label(gt_label_file, init_label_file, combined_label_file, J = 16):
    # read lables
    with open(gt_label_file, 'r') as f:
        gt_labels = f.readlines()
    print len(gt_labels)
    with open(init_label_file, 'r') as f:
        init_labels = f.readlines()
    print len(init_labels)

    combined_poses = np.zeros((len(gt_labels), J * 3 * 2), dtype=float)
    for idx in xrange(len(gt_labels)):
        # get pose
        gt_pose = map(float, gt_labels[idx].split())
        gt_pose = np.asarray(gt_pose)
        init_pose = map(float, init_labels[idx].split())
        init_pose = np.asarray(init_pose)
        combined_poses[idx] = np.concatenate((gt_pose, init_pose), axis=0)
    np.savetxt(combined_label_file, combined_poses, fmt='%1.3f')
    # with open(combined_label_file, 'w') as f:
    #     for i in range(len(combined_poses)):
    #         for j in range(combined_poses[i].shape[0]):
    #             f.write('{:.3f} '.format(combined_poses[i][j]))
    #         f.write('\n')


def combine_two_files(file1, file2, combined_file):
    filenames = [file1, file2]
    with open(combined_file, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


def combine_files(files, combined_file, new_line=False):
    with open(combined_file, 'w') as outfile:
        for fname in files:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
            if new_line:
                outfile.write('\n')


def make_output_pose_command(output_pose_bin, model, weights, label_list, output_name, fx, fy, ux, uy, iter, gpu_id, log_suffix):
    command = '{0} \
    --model={1} \
    --gpu={10} \
    --weights={2} \
    --label_list={3} \
    --output_name={4} \
    --fx={5} \
    --fy={6} \
    --ux={7} \
    --uy={8} \
    2>&1 | tee {11}_iter{9}.txt'.format(output_pose_bin, model, weights, label_list, output_name, fx, fy, ux,
                                                 uy, iter, gpu_id, log_suffix)
    return command


def get_connect_structure(dataset):
    if dataset == 'icvl':
        return [[0,1,3], [0,4,6], [0,7,9], [0,10,12], [0,13,15]]
    elif dataset == 'nyu':
        return [[0,5,3], [0,13,12], [0,11,10], [0,9,8], [0,7,6]]
    elif dataset == 'msra':
        return [[0,2,4], [0,6,8], [0,10,12], [0,14,16], [0,18,20]]


def get_guided_joints(dataset):
    if dataset == 'icvl':
        return [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15]
    elif dataset == 'nyu':
        return [0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    elif dataset == 'msra':
        return [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]